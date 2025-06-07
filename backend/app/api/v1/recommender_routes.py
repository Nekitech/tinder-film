from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status

from app.core.deps import get_ml_recommender_service
from app.schemas.recommender import RecommendationResponse
from app.services.ml_recommender import RecommenderService

recommender_router = APIRouter()


class CreateRatingRequest(BaseModel):
    user_id: int = Field(..., description="ID юзера")
    movie_id: int = Field(..., description="ID фильма")
    rating: float = Field(..., gt=0.0, le=5.0, description="Оценка от 1.0 до 5.0")


class CreateRatingResponse(BaseModel):
    user_id: int
    movie_id: int
    rating: float


@recommender_router.post("/train", status_code=200)
async def train_recommender(
        limit: int = 500,
        recommender_service: RecommenderService = Depends(get_ml_recommender_service),
):
    """
    Эндпоинт для обучения рекомендательной модели.

    :param limit: Максимальное количество строк для выборки из БД, по умолчанию 500.
    :param recommender_service: Сервис рекомендательной системы.
    :return: Сообщение об успешном завершении обучения.
    """
    await recommender_service.train_model(limit=limit)
    return {"message": "Model trained successfully"}


@recommender_router.get("/recommendations/{user_id}", response_model=RecommendationResponse,
                        response_model_exclude_none=True)
async def recommend(
        user_id: int,
        n: int = 5,
        limit: int = 500,
        recommender_service: RecommenderService = Depends(get_ml_recommender_service),
):
    """
    Эндпоинт для получения рекомендаций для пользователя.

    :param user_id: ID пользователя.
    :param n: Максимальное количество рекомендаций.
    :param limit: Максимальное количество строк для выборки из БД, по умолчанию 500.
    :param recommender_service: Сервис рекомендательной системы.
    :return: Топ-N рекомендаций для пользователя.
    """
    recommender_service.load_model()
    recommendations = await recommender_service.get_top_n(user_id=user_id, n=n, limit=limit)
    return {"user_id": user_id, "recommendations": recommendations}


@recommender_router.post("/ratings", response_model=CreateRatingResponse)
async def create_rating(
        request: CreateRatingRequest,
        recommender_service: RecommenderService = Depends(get_ml_recommender_service)
):
    """
    POST-обработчик для создания новой оценки.
    :param recommender_service:
    :param request: Данные для создания оценки
    :param user_id: ID пользователя (автоматически определяется)
    :param rating_service: Сервис для работы с оценками
    :return: Новая запись оценки
    """
    try:
        rating = await recommender_service.create_rating(
            user_id=request.user_id,
            movie_id=request.movie_id,
            rating=request.rating
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return rating

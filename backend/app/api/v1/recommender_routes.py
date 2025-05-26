from fastapi import APIRouter, Depends

from app.core.deps import get_ml_recommender_service
from app.schemas.recommender import RecommendationResponse
from app.services.ml_recommender import RecommenderService

recommender_router = APIRouter()


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


@recommender_router.get("/recommendations/{user_id}", response_model=RecommendationResponse)
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
    print(recommendations)
    return {"user_id": user_id, "recommendations": recommendations}

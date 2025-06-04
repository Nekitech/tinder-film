from fastapi import APIRouter, Depends

from app.core.deps import get_similar_users_service
from app.schemas.similar_user import SimilarUsersResponse
from app.services.ml_similar_user import SimilarUsersService

router = APIRouter()


@router.post("/train", status_code=200, tags=["Similar Users"])
async def train_similar_users_model(
        limit: int = 500,
        k: int = 5,
        similar_users_service: SimilarUsersService = Depends(get_similar_users_service)
):
    """
    Эндпоинт для обучения модели поиска похожих пользователей.

    :param limit: Ограничение по количеству строк из БД.
    :param k: Количество ближайших соседей.
    :param similar_users_service: Сервис для поиска похожих пользователей.
    :return: Успешное сообщение.
    """
    await similar_users_service.train_model(limit=limit, k=k)
    return {"message": "KNN model trained successfully"}


@router.get("/similar-users/{user_id}", response_model=SimilarUsersResponse, tags=["Similar Users"])
async def get_similar_users(
        user_id: int,
        n: int = 5,
        similar_users_service: SimilarUsersService = Depends(get_similar_users_service)
):
    """
    Эндпоинт для получения списка похожих пользователей.

    :param user_id: ID пользователя.
    :param n: Сколько пользователей вернуть.
    :param similar_users_service: Сервис для поиска похожих пользователей.
    :return: Список ID похожих пользователей.
    """
    await similar_users_service.load_model()
    similar_user_ids = await similar_users_service.get_similar_users(user_id=user_id, n=n)
    return {"user_id": user_id, "similar_users": similar_user_ids}

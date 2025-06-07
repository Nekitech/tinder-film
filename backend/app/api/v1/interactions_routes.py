from fastapi import APIRouter, Depends, status

from app.core.deps import get_interaction_service
from app.services.interactions import InteractionsService

router = APIRouter()


@router.post("/interactions/like_or_dislike", tags=["Interactions"], status_code=status.HTTP_200_OK)
async def like_or_dislike_interaction(
        user_id: int,
        movie_id: int,
        liked: bool,
        service: InteractionsService = Depends(get_interaction_service),
):
    """
    Обработка лайка или дизлайка фильма от пользователя
    """
    interaction = await service.like_or_dislike(user_id=user_id, movie_id=movie_id, liked=liked)
    return {"id": interaction.id, "user_id": interaction.user_id, "movie_id": interaction.movie_id,
            "liked": interaction.liked}


@router.get("/interactions/user/{user_id}", tags=["Interactions"])
async def get_user_interactions(
        user_id: int,
        service: InteractionsService = Depends(get_interaction_service),
):
    """
    Получение всех взаимодействий пользователя
    """
    return await service.get_user_interactions(user_id)


@router.get("/interactions/movie/{movie_id}", tags=["Interactions"])
async def get_movie_interactions(
        movie_id: int,
        service: InteractionsService = Depends(get_interaction_service),
):
    """
    Получение всех взаимодействий с фильмом
    """
    return await service.get_movie_interactions(movie_id)

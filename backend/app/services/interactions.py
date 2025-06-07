from app.db.interactioins import InteractionsRepository


class InteractionsService:
    def __init__(self, repository: InteractionsRepository):
        self.repo = repository

    async def like_or_dislike(self, user_id: int, movie_id: int, liked: bool):
        # Проверяем, существует ли уже взаимодействие
        existing_interaction = await self.repo.get_interaction(user_id, movie_id)
        if existing_interaction:
            # Обновление существующего взаимодействия
            existing_interaction.liked = liked
            await self.repo.db.commit()
            return existing_interaction
        else:
            # Добавление нового взаимодействия
            return await self.repo.add_interaction(user_id, movie_id, liked)

    async def get_user_interactions(self, user_id: int):
        return await self.repo.get_user_interactions(user_id)

    async def get_movie_interactions(self, movie_id: int):
        return await self.repo.get_movie_interactions(movie_id)

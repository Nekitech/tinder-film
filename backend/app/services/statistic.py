from typing import List, Dict

from app.db.statistic import StatisticRepo


class StatisticService:

    def __init__(self, repo: StatisticRepo):
        self.repo = repo

    async def get_top_films(self, user_id: int):
        return await self.repo.get_top_movies_by_user_id(user_id)

    async def get_top_genres(self, user_id: int) -> List[Dict]:
        return await self.repo.get_top_genres_by_user_id(user_id)

    async def get_similar_users(self, user_id: int) -> List[Dict]:
        return await self.repo.get_similar_users(user_id)

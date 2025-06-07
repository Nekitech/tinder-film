from collections import Counter
from typing import List, Dict

import pandas as pd
from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from surprise import Reader, Dataset, KNNBasic

from app.db.models import Movie, Rating


class StatisticRepo:
    def __init__(self, db: AsyncSession):
        self.db = db
        pass

    async def get_top_movies_by_user_id(self, user_id: int, limit: int = 10) -> List[Dict]:
        stmt = (
            select(Movie.id, Movie.title, Rating.rating)
            .join(Rating, Rating.movie_id == Movie.id)
            .where(Rating.user_id == user_id)
            .order_by(desc(Rating.rating))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return [
            {"movie_id": row.id, "title": row.title, "rating": row.rating}
            for row in result.fetchall()
        ]

    async def get_top_genres_by_user_id(self, user_id: int, limit: int = 5) -> List[Dict]:
        stmt = (
            select(Movie.genres)
            .join(Rating, Rating.movie_id == Movie.id)
            .where(Rating.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        genres_list = [
            genre.strip()
            for row in result.fetchall()
            for genre in (row.genres or "").split("|")
        ]
        most_common = Counter(genres_list).most_common(limit)
        return [{"genre": genre, "count": count} for genre, count in most_common]

    async def get_similar_users(self, user_id: int, limit: int = 5) -> List[Dict]:
        # Загружаем рейтинги из БД
        stmt = select(Rating.user_id, Rating.movie_id, Rating.rating)
        result = await self.db.execute(stmt)
        df = pd.DataFrame(result.fetchall(), columns=["user_id", "movie_id", "rating"])

        if df.empty or user_id not in df["user_id"].values:
            return []

        # Создаём dataset для Surprise
        reader = Reader(rating_scale=(df["rating"].min(), df["rating"].max()))
        data = Dataset.load_from_df(df[["user_id", "movie_id", "rating"]], reader)

        # Обучаем модель KNN (user-based)
        trainset = data.build_full_trainset()
        sim_options = {
            "name": "cosine",
            "user_based": True,
        }
        algo = KNNBasic(sim_options=sim_options)
        algo.fit(trainset)

        # Получаем внутренний id пользователя в trainset
        try:
            inner_id = trainset.to_inner_uid(user_id)
        except ValueError:
            return []

        # Получаем топ-N похожих пользователей
        neighbors = algo.get_neighbors(inner_id, k=limit)

        # Преобразуем внутренние id обратно во внешние
        similar_users = [
            {"user_id": int(trainset.to_raw_uid(inner_id_neighbor))}
            for inner_id_neighbor in neighbors
        ]

        return similar_users

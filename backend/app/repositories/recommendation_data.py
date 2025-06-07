import time
from typing import List, Dict

import pandas as pd
from sqlalchemy import Table, Column, Integer, Float, MetaData, String
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

metadata = MetaData()

# Декларация таблицы через SQLAlchemy Table
ratings_table = Table(
    "ratings",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("movie_id", Integer, nullable=False),
    Column("rating", Float, nullable=False),
    Column("timestamp", Integer, nullable=False)
)

movies_table = Table(
    "movies",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False)
)


class RecommenderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_ratings_df(self, limit: int = 1000) -> pd.DataFrame:
        """
        Загружает оценки пользователей из базы данных.
        """
        result = await self.db.execute(
            select(
                ratings_table.c.user_id,
                ratings_table.c.movie_id,
                ratings_table.c.rating
            ).limit(limit)
        )
        rows = result.fetchall()
        return pd.DataFrame(rows, columns=["user_id", "movie_id", "rating"])

    async def get_movie_titles(self, movie_ids: List[int]) -> Dict[int, str]:
        """
        Возвращает словарь movie_id -> title по списку ID.
        """
        result = await self.db.execute(
            select(movies_table.c.id, movies_table.c.title)
            .where(movies_table.c.id.in_(movie_ids))
        )
        rows = result.mappings().all()
        return {row["id"]: row["title"] for row in rows}

    async def create_rating(self, user_id: int, movie_id: int, rating: float):
        """
        Создает новую запись в таблице ratings.
        :param user_id: ID пользователя
        :param movie_id: ID фильма
        :param rating: Оценка пользователя (1.0-5.0)
        :return: Словарь с информацией о добавленной записи
        """
        timestamp = int(time.time())

        query = ratings_table.insert().values(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating,
            timestamp=timestamp
        ).returning(
            ratings_table.c.user_id,
            ratings_table.c.movie_id,
            ratings_table.c.rating,
            ratings_table.c.timestamp
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.fetchone()

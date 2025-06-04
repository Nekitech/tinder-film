import pandas as pd
from sqlalchemy import Table, Column, Integer, Float, MetaData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

metadata = MetaData()

ratings_table = Table(
    "ratings",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("movie_id", Integer, nullable=False),
    Column("rating", Float, nullable=False)
)


class SimilarUsersRepository:
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

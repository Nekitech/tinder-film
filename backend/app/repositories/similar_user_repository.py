import pandas as pd
from sqlalchemy import Table, Column, Integer, Float, MetaData, String
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

users_table = Table(
    "users",  # Assuming the table name is 'users'
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=True)
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

    async def get_usernames_by_ids(self, user_ids: list[int]) -> list[dict[str, object]]:
        """
        Получает username для переданных ID пользователей.
        Если username отсутствует, устанавливается null.
        :param user_ids: Список ID пользователей.
        :return: Список словарей с user_id и username.
        """
        result = await self.db.execute(
            select(
                users_table.c.id.label("user_id"),
                users_table.c.username
            ).where(users_table.c.id.in_(user_ids))
        )

        rows = result.fetchall()

        # Создадим словарь, сопоставляющий user_id с username
        user_dict = {row.user_id: row.username for row in rows}

        # Вернем список словарей с установленным null для отсутствующих пользователей
        return [{"user_id": user_id, "username": user_dict.get(user_id)} for user_id in user_ids]

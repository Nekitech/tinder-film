from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Interaction


class InteractionsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_interaction(self, user_id: id, movie_id: int, liked: bool):
        interaction = Interaction(
            user_id=user_id,
            movie_id=movie_id,
            liked=liked,
        )
        self.db.add(interaction)
        await self.db.commit()
        return interaction

    async def get_user_interactions(self, user_id: id):
        query = select(Interaction).where(Interaction.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_movie_interactions(self, movie_id: int):
        query = select(Interaction).where(Interaction.movie_id == movie_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_interaction(self, user_id: id, movie_id: int):
        query = (
            select(Interaction)
            .where(
                Interaction.user_id == user_id,
                Interaction.movie_id == movie_id,
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_interactions(self):
        query = select(Interaction)
        result = await self.db.execute(query)
        return result.scalars().all()

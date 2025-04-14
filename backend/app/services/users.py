from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password="asdasd"
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

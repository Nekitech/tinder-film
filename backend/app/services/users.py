from typing import List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.user import UserCreate, UserOut


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_name(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(
            username=user_create.username,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> UserOut | None:
        """Получить пользователя по его ID."""
        query = select(User).where(User.id == user_id)
        try:
            result = await self.db.execute(query)
            return result.scalar_one()
        except NoResultFound:
            return None

    async def get_users(self, skip: int = 0, limit: int = 10) -> List[UserOut]:
        """Получить список пользователей с пагинацией."""
        query = select(User).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete_user(self, user_id: int) -> bool:
        """Удалить пользователя по ID. Возвращает True, если удаление успешно, иначе False."""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def update_user(self, user_id: int, username: str) -> UserOut:
        """Обновить имя пользователя."""
        user = await self.get_user_by_id(user_id)
        if user:
            user.username = username
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        raise NoResultFound("User not found")

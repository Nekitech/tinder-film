import os
from datetime import timedelta

import bcrypt
from authx import RequestToken, AuthX
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import UserCredentials, User


class AuthService:
    def __init__(self, db: AsyncSession, auth: AuthX):
        self.db = db
        self.auth = auth

    async def register_user(self, username: str, password: str):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(16))
        user = User(username=username)

        self.db.add(user)
        await self.db.flush()  # Получить user.id до коммита

        creds = UserCredentials(user_id=user.id, hashed_password=hashed.decode())
        self.db.add(creds)

        await self.db.commit()
        return user

    async def login(self, username: str, password: str):
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        if not user:
            return None
        creds = user.credentials
        if not bcrypt.checkpw(password.encode(), creds.hashed_password.encode()):
            return None

        access_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
        refresh_expires = timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))

        access_token = self.auth.create_access_token(str(user.id), expiry=access_expires)
        refresh_token = self.auth.create_refresh_token(str(user.id), expiry=refresh_expires)

        creds.access_token = access_token
        creds.refresh_token = refresh_token
        await self.db.commit()

        return creds.access_token, creds.refresh_token

    async def refresh_access_token(self, refresh_token: RequestToken) -> str:
        # Проверка refresh_token
        payload = self.auth.verify_token(refresh_token, verify_csrf=False)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        user_id = payload.sub

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        # Генерация новых токенов
        access_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))

        access_token = self.auth.create_access_token(str(user_id), expiry=access_expires)

        # Обновляем в БД
        # creds = await self.db.get(UserCredentials, int(user_id))
        creds = UserCredentials(user_id=int(user_id))
        creds.access_token = access_token
        await self.db.commit()

        return access_token

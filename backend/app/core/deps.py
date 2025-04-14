import os

from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_session
from app.services.auth import AuthService
from app.services.users import UserService

load_dotenv()


def get_authx() -> AuthX:
    config = AuthXConfig(
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    )

    authx = AuthX(config)
    return authx


def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(db)


def get_auth_service(db: AsyncSession = Depends(get_session), auth: AuthX = Depends(get_authx)) -> AuthService:
    return AuthService(db, auth)

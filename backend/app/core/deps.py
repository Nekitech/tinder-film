import os

from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_session
from app.services.auth import AuthService
from app.services.ml_recommender import RecommenderService
from app.services.users import UserService
from app.utils.model_storage import ModelStorage

load_dotenv()

MODEL_PATH = "app/models/trained_model.pkl"


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


def get_model_storage() -> ModelStorage:
    return ModelStorage(MODEL_PATH)


def get_ml_recommender_service(db: AsyncSession = Depends(get_session),
                               model_storage: ModelStorage = Depends(get_model_storage)) -> RecommenderService:
    return RecommenderService(db, model_storage)

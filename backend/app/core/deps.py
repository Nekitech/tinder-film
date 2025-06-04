import os

from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_session
from app.db.statistic import StatisticRepo
from app.repositories.recommendation_data import RecommenderRepository
from app.repositories.similar_user_repository import SimilarUsersRepository
from app.schemas.auth import AuthJWT
from app.services.auth import AuthService
from app.services.auth_jwt import AuthJWTService
from app.services.ml_recommender import RecommenderService
from app.services.ml_similar_user import SimilarUsersService
from app.services.statistic import StatisticService
from app.services.users import UserService
from app.utils.model_storage import ModelStorage

load_dotenv()

MODEL_PATH_SVD = "app/models/trained_model_recommender.pkl"
MODEL_PATH_KNNBasic = "app/models/trained_model_similar_user.pkl"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)


def get_authx() -> AuthX:
    config = AuthXConfig(
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    )

    authx = AuthX(config)
    return authx


def get_auth_jwt() -> AuthJWT:
    return AuthJWT()


def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(db)


def get_auth_service(db: AsyncSession = Depends(get_session), auth: AuthX = Depends(get_authx)) -> AuthService:
    return AuthService(db, auth)


def get_auth_jwt_service(db: AsyncSession = Depends(get_session),
                         auth: AuthJWT = Depends(get_auth_jwt),
                         user_service: UserService = Depends(get_user_service)
                         ) -> AuthJWTService:
    return AuthJWTService(db, auth, user_service)


def get_model_storage_svd() -> ModelStorage:
    return ModelStorage(MODEL_PATH_SVD)


def get_model_storage_knnbasic() -> ModelStorage:
    return ModelStorage(MODEL_PATH_KNNBasic)


async def get_recommender_repository(
        db: AsyncSession = Depends(get_session)
) -> RecommenderRepository:
    return RecommenderRepository(db)


def get_ml_recommender_service(
        repo: RecommenderRepository = Depends(get_recommender_repository),
        storage: ModelStorage = Depends(get_model_storage_svd),
) -> RecommenderService:
    return RecommenderService(repository=repo, model_storage=storage)


# def get_implicit_feedback_service(
#         repo: RecommenderRepository = Depends(get_recommender_repository),
#         model_storage: ModelStorage = Depends(get_model_storage),
# ) -> ImplicitFeedbackService:
#     return ImplicitFeedbackService(repository=repo, model_storage=model_storage)


async def get_current_auth_user_for_refresh(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthJWTService = Depends(get_auth_jwt_service),
):
    payload = await auth_service.get_current_token_payload(token)  # Разбор текущего токена
    auth_service.validate_token_type(payload, token_type=auth_service.REFRESH_TOKEN_TYPE)  # Проверяем тип токена
    user = await auth_service.user_service.get_user_by_id(int(payload.get('sub')))  # Получение пользователя
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


def get_statistic_repository(db: AsyncSession = Depends(get_session)) -> StatisticRepo:
    return StatisticRepo(db)


def get_statistic_service(repo: StatisticRepo = Depends(get_statistic_repository)) -> StatisticService:
    return StatisticService(repo)


def get_repo_similar_user(db: AsyncSession = Depends(get_session)):
    return SimilarUsersRepository(db)


def get_similar_users_service(model: ModelStorage = Depends(get_model_storage_knnbasic),
                              repo: SimilarUsersRepository = Depends(get_repo_similar_user)) -> SimilarUsersService:
    return SimilarUsersService(repo, model)

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from starlette import status

from app.core.deps import get_auth_jwt_service, get_current_auth_user_for_refresh
from app.db.models import User
from app.schemas.auth import TokenInfo, LoginRequest
from app.schemas.user import UserLogin, PayloadUser
from app.services.auth_jwt import AuthJWTService

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    dependencies=[Depends(http_bearer)]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)


@router.post("/register", tags=["Auth"], status_code=status.HTTP_201_CREATED)
async def register(username: str, password: str, service: AuthJWTService = Depends(get_auth_jwt_service)):
    return await service.register_user(username, password)


@router.post("/login", tags=["Auth"], response_model=TokenInfo, status_code=status.HTTP_200_OK)
async def login(user: LoginRequest,
                service: AuthJWTService = Depends(get_auth_jwt_service)):
    return await service.login(UserLogin(username=user.username, password=user.password))


@router.post(
    "/refresh/",
    tags=["Auth"],
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
        user: User = Depends(get_current_auth_user_for_refresh),  # Берём юзера из зависимости
        auth_service: AuthJWTService = Depends(get_auth_jwt_service),  # Берём сервис для работы с JWT
):
    access_token = await auth_service.create_access_token(user)  # Создаём access token
    return TokenInfo(access_token=access_token)  # Возвращаем результат


@router.get("/users/me/", tags=["Auth"], response_model=PayloadUser, status_code=status.HTTP_200_OK)
async def auth_user_check_self_info(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthJWTService = Depends(get_auth_jwt_service),
):
    payload = await auth_service.get_current_token_payload(token)
    return payload

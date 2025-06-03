from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from app.core.deps import get_auth_jwt_service
from app.schemas.auth import TokenInfo
from app.schemas.user import UserLogin, PayloadUser
from app.services.auth_jwt import AuthJWTService

http_bearer = HTTPBearer(auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)

router = APIRouter(
    dependencies=[Depends(http_bearer)]
)


# @router.post("/register", tags=["Auth"], status_code=status.HTTP_201_CREATED)
# async def register(username: str, password: str, service: AuthService = Depends(get_auth_service)):
#     return await service.register_user(username, password)
#
#
# @router.post("/login", tags=["Auth"], response_model=LoginResponse, status_code=status.HTTP_200_OK)
# async def login(payload: UserLogin, response: Response, service: AuthService = Depends(get_auth_service)):
#     access_token = await service.login(payload.username, payload.password)
#
#     if not access_token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#
#     response.set_cookie("access_token",
#                         access_token,
#                         httponly=True,
#                         expires=3600,
#                         samesite="none",
#                         secure=True
#                         )
#
#     return {
#         "code": status.HTTP_200_OK,
#         "access_token": access_token,
#     }


# @router.post("/refresh", tags=["Auth"], dependencies=[Depends(get_authx().get_token_from_request)],
#              status_code=status.HTTP_200_OK)
# async def refresh_tokens(
#         response: Response,
#         refresh_token: RequestToken = Depends(),
#         service: AuthService = Depends(get_auth_service),
#
# ):
#     access_token = await service.refresh_access_token(refresh_token)
#     response.set_cookie("access_token", access_token, httponly=True, max_age=60 * 15)
#     return access_token
#
#
# @router.get("/token", tags=["Auth"], status_code=status.HTTP_200_OK)
# async def get_access_token_from_cookie(access_token: str = Cookie(None)):
#     if not access_token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found in cookies")
#     return {"access_token": access_token}


# JWT Auth

@router.post("/register", tags=["Auth"], status_code=status.HTTP_201_CREATED)
async def register(username: str, password: str, service: AuthJWTService = Depends(get_auth_jwt_service)):
    return await service.register_user(username, password)


@router.post("/login", tags=["Auth"], response_model=TokenInfo, status_code=status.HTTP_200_OK)
async def login(user: OAuth2PasswordRequestForm = Depends(),
                service: AuthJWTService = Depends(get_auth_jwt_service)):
    return await service.login(UserLogin(username=user.username, password=user.password))


@router.get("/users/me/", tags=["Auth"], response_model=PayloadUser, status_code=status.HTTP_200_OK)
async def auth_user_check_self_info(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthJWTService = Depends(get_auth_jwt_service),
):
    payload = await auth_service.get_current_token_payload(token)
    return payload

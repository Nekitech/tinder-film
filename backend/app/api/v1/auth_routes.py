from authx import RequestToken
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie

from app.core.deps import get_auth_service, get_authx
from app.schemas.user import UserLogin
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", tags=["Auth"])
async def register(username: str, password: str, service: AuthService = Depends(get_auth_service)):
    return await service.register_user(username, password)


@router.post("/login", tags=["Auth"])
async def login(payload: UserLogin, response: Response, service: AuthService = Depends(get_auth_service)):
    access_token = await service.login(payload.username, payload.password)

    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response.set_cookie("access_token",
                        access_token,
                        httponly=True,
                        expires=3600,
                        samesite="none",
                        secure=True
                        )

    return {
        "code": 200,
        "access_token": access_token,
    }


@router.post("/refresh", tags=["Auth"], dependencies=[Depends(get_authx().get_token_from_request)])
async def refresh_tokens(
        response: Response,
        refresh_token: RequestToken = Depends(),
        service: AuthService = Depends(get_auth_service),

):
    access_token = await service.refresh_access_token(refresh_token)
    response.set_cookie("access_token", access_token, httponly=True, max_age=60 * 15)
    return access_token


@router.get("/token", tags=["Auth"])
async def get_access_token_from_cookie(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found in cookies")
    return {"access_token": access_token}

from authx import RequestToken
from fastapi import APIRouter, Depends, HTTPException, Response

from app.core.deps import get_auth_service, get_authx
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", tags=["Auth"])
async def register(username: str, password: str, service: AuthService = Depends(get_auth_service)):
    return await service.register_user(username, password)


@router.post("/login", tags=["Auth"])
async def login(username: str, password: str, response: Response, service: AuthService = Depends(get_auth_service)):
    access_token, refresh_token = await service.login(username, password)

    if not access_token or not refresh_token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print(access_token)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return {"code": 200,
            "access_token": access_token,
            "refresh_token": refresh_token
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

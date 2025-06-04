from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, HTTPException, Query

from app.core.deps import get_user_service
from app.schemas.user import UserOut, UserCreate
from app.services.users import UserService

router = APIRouter()


@router.post("/users/", response_model=UserOut, tags=["Users 🧘"])
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(user)


@router.get("/users/{user_id}", response_model=UserOut, tags=["Users 🧘"])
async def get_user_by_id(
        user_id: Annotated[
            int, Path(..., title="ID пользователя", description="Уникальный идентификатор пользователя")],
        service: UserService = Depends(get_user_service),
):
    """Получить пользователя по его ID."""
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=List[UserOut], tags=["Users 🧘"])
async def get_users(
        skip: Annotated[int, Query(ge=0, description="Количество пропускаемых пользователей")] = 0,
        limit: Annotated[int, Query(ge=1, le=100, description="Количество пользователей для возврата")] = 10,
        service: UserService = Depends(get_user_service),
):
    """Получение списка пользователей с пагинацией."""
    return await service.get_users(skip=skip, limit=limit)


@router.delete("/users/{user_id}", tags=["Users 🧘"])
async def delete_user(
        user_id: Annotated[
            int, Path(..., title="ID пользователя", description="Уникальный идентификатор пользователя")
        ],
        service: UserService = Depends(get_user_service),
):
    """Удалить пользователя по ID."""
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@router.patch("/users/{user_id}", response_model=UserOut, tags=["Users 🧘"])
async def update_user_username(
        user_id: Annotated[
            int, Path(..., title="ID пользователя", description="Уникальный идентификатор пользователя")],
        username: Annotated[str, Query(..., max_length=50, description="Новое имя пользователя")],
        service: UserService = Depends(get_user_service),
):
    """Обновить имя пользователя."""
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await service.update_user(user_id, username=username)

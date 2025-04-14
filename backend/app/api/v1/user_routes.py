from fastapi import APIRouter, Depends

from app.core.deps import get_user_service
from app.schemas.user import UserOut, UserCreate
from app.services.users import UserService

router = APIRouter()


@router.post("/users/", response_model=UserOut, tags=["Users 🧘"])
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(user)

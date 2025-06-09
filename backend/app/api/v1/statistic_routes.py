from fastapi import APIRouter
from fastapi.params import Depends

from app.core.deps import get_statistic_service
from app.services.statistic import StatisticService

router = APIRouter()


@router.get("/statistic/top_films", tags=["statistic"])
async def get_statistic_top_films(user_id: int,
                                  statistic_service: StatisticService = Depends(get_statistic_service)):
    return await statistic_service.get_top_films(user_id)


@router.get("/statistic/top_genres", tags=["statistic"])
async def get_statistic_top_genres(
        user_id: int,
        statistic_service: StatisticService = Depends(get_statistic_service)
):
    return await statistic_service.get_top_genres(user_id)

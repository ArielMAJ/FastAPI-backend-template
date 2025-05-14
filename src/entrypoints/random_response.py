from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.schemas.random_number import RandomResponse
from src.services.random_number_service import RandomResponseService

router = APIRouter()


@router.get("/", response_model=RandomResponse)
@cache(expire=5)
async def random_number():
    """
    Sends random number back to user.

    :returns: random number to user.
    """
    return await RandomResponseService.get_random_number()

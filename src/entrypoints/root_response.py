from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.schemas.root_response import RootResponse
from src.services.root_response_service import RootResponseService

router = APIRouter()


@router.get("/", response_model=RootResponse)
@cache(expire=5)
async def root_response():
    """
    Sends root response back to user.

    :returns: root response to user.
    """
    return await RootResponseService.get_root_response()

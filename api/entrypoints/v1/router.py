from api.entrypoints.v1 import random_number, root_response, user
from fastapi.routing import APIRouter

router = APIRouter()
router.include_router(
    random_number.router, prefix="/random_number", tags=["Random Number"]
)
router.include_router(root_response.router, prefix="", tags=["Root Response"])
router.include_router(user.router, prefix="/user", tags=["User"])

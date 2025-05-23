from fastapi.routing import APIRouter

from src.entrypoints import auth, monitoring, random_response, root_response, user

router = APIRouter()
router.include_router(monitoring.router, tags=["Monitoring"])
router.include_router(
    random_response.router, prefix="/random_number", tags=["Random Number"]
)
router.include_router(root_response.router, prefix="", tags=["Root Response"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])

__all__ = ["router"]

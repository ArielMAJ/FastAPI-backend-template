from pathlib import Path

from api.config import Config
from api.entrypoints.router import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

# from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

APP_ROOT = Path(__file__).parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    _app = FastAPI(
        title="fastapi-backend-template",
        # default_response_class=JSONResponse,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=Config.DATABASE.POSTGRES_URI,
        engine_args={
            "echo": True,
            "pool_pre_ping": True,
            "pool_size": 5,
            "max_overflow": 10,
        },
        commit_on_exit=True,
    )
    _app.include_router(router=api_router)

    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    return _app

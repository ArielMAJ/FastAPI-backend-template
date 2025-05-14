import pytest
from httpx import ASGITransport, AsyncClient

from src.app import get_app, lifespan


@pytest.fixture(scope="session")
def anyio_backend():
    """This fixture sets up asyncio as the async backend."""
    return "asyncio"


@pytest.fixture(scope="function")
async def client():
    app = get_app()
    async with lifespan(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client

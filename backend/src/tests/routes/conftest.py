import pytest, pytest_asyncio, sys, asyncio
from httpx import AsyncClient

from src.api import app
from src.config.config_db import Base, test_async_session, test_engine
from src.middleware.utils_db import get_session
from src.middleware.utils_environment import get_environment_config
from src.middleware.security import hash_password
from src.models.user_model import User

config = get_environment_config()

async def override_get_session():
    async with test_async_session() as session:
        yield session

@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def session():
    async with test_async_session() as session:
        yield session

@pytest_asyncio.fixture
async def test_app():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Seed the default admin user for authentication tests
    async with test_async_session() as session:
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("@Test2026"),
            is_active=True,
        )
        session.add(admin)
        await session.commit()

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app) as client:
        yield client

@pytest_asyncio.fixture
async def test_app_authentication(test_app, session):
    BACKEND_URL = config.get('BACKEND_URL') + 'login/'
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = "username=admin&password=%40Test2026"

    token = await test_app.post(BACKEND_URL, content = body, headers = headers)

    yield token
from typing import Any, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from service_platform_py.api.application import get_app
from service_platform_py.api.router.user.manager import UserManager
from service_platform_py.db.user.repository import UserRepository
from service_platform_py.service.postgres.dependency import (
    create_database,
    drop_database,
    get_db_session,
    migrate,
)
from service_platform_py.settings import Environment, settings


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    if settings.environment == Environment.TEST:
        await create_database()

    engine = create_async_engine(str(settings.postgres_url))
    async with engine.begin():
        if settings.environment == Environment.TEST:
            migrate()
    try:
        yield engine
    finally:
        await engine.dispose()
        if settings.environment == Environment.TEST:
            await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def api(
    dbsession: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    api: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=api, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def user_repository(
    dbsession: AsyncSession,
) -> UserRepository:
    return UserRepository(dbsession)


@pytest.fixture
def user_manager(
    user_repository: UserRepository,
) -> UserManager:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    return UserManager(user_repository)

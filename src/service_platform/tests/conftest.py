import asyncio
from io import BytesIO
from typing import Any, AsyncGenerator
from unittest.mock import patch

import pytest
from faker import Faker
from fastapi import FastAPI, UploadFile
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from service_platform.api.application import get_app
from service_platform.api.manager.user.manager import UserManager
from service_platform.client.model.auth_provider import AuthProvider
from service_platform.client.request.auth.auth_request import RefreshTokenRequest
from service_platform.core.security.custom_authentication import CustomAuthentication
from service_platform.core.security.jwt_claim_generator import JWTClaimGenerator
from service_platform.core.security.jwt_registered_claim import JWTRegisteredClaim
from service_platform.core.security.jwt_token_generator import JWTTokenGenerator
from service_platform.db.refresh_token.repository import RefreshTokenRepository
from service_platform.db.user.repository import UserRepository
from service_platform.db.user.table import UserEntity
from service_platform.service.aws.s3 import S3
from service_platform.service.aws.sqs import SQSConsumer, SQSJobProducer
from service_platform.service.postgres.dependency import get_db_session
from service_platform.settings import settings
from service_platform.worker.example_worker.processor import ExampleWorkerProcessor
from service_platform.worker.example_worker.repository.respository import (
    ExampleWorkerRepository,
)

fake = Faker()

DEFAULT_USER_NAME = fake.user_name()
DEFAULT_USER_EMAIL = fake.email()
DEFAULT_USER_ID = fake.uuid4()
DEFAULT_USER_PICTURE = fake.image_url()


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
    engine = create_async_engine(str(settings.postgres_url))
    try:
        yield engine
    finally:
        await engine.dispose()


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
        class_=AsyncSession,
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
def refresh_token_repository(
    dbsession: AsyncSession,
) -> RefreshTokenRepository:
    return RefreshTokenRepository(dbsession)


@pytest.fixture
def example_worker_repository(
    dbsession: AsyncSession,
) -> ExampleWorkerRepository:
    example_worker_repository = ExampleWorkerRepository()
    example_worker_repository.database = dbsession
    return example_worker_repository


@pytest.fixture
def user_manager(
    user_repository: UserRepository,
) -> UserManager:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    return UserManager(user_repository)


@pytest.fixture
async def test_user(
    user_repository: UserRepository,
) -> UserEntity:
    return await user_repository.insert_user(
        auth_id=DEFAULT_USER_ID,
        email=DEFAULT_USER_EMAIL,
        name=DEFAULT_USER_NAME,
        picture_url=DEFAULT_USER_ID,
        auth_provider=AuthProvider.GOOGLE,
    )


@pytest.fixture
def claim_generator() -> JWTClaimGenerator:
    return JWTClaimGenerator(
        registered_claim=JWTRegisteredClaim(),
    )


@pytest.fixture
def token_generator(
    claim_generator: JWTClaimGenerator,
) -> JWTTokenGenerator:
    return JWTTokenGenerator(
        claim_generator=claim_generator,
    )


@pytest.fixture
async def access_token(
    test_user: UserEntity,
    token_generator: JWTTokenGenerator,
) -> str:
    """
    Fixture to create an access token for the test user.
    """
    authentication = CustomAuthentication(
        user_id=str(test_user.id),
        roles=[test_user.roles],
    )
    jwt_token = token_generator.generate_token(authentication)
    return jwt_token.access_token


@pytest.fixture
async def authenticated_client(client: AsyncClient, access_token: str) -> AsyncClient:
    """
    Fixture to create an authenticated client.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}",
    }
    return client


@pytest.fixture
async def refresh_token(
    test_user: UserEntity,
    token_generator: JWTTokenGenerator,
    refresh_token_repository: RefreshTokenRepository,
) -> str:
    """
    Fixture to create a refresh token for the test user.
    """

    refresh_token = await refresh_token_repository.create(
        RefreshTokenRequest(user_id=test_user.id)
    )
    authentication = CustomAuthentication(
        user_id=str(test_user.id), roles=[test_user.roles], jti=str(refresh_token.id)
    )
    jwt_token = token_generator.generate_token(authentication)
    return jwt_token.refresh_token


@pytest.fixture
async def authenticated_client_with_refresh_token(
    client: AsyncClient, refresh_token: str
) -> AsyncClient:
    """
    Fixture to create an authenticated client with both access and refresh tokens.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {refresh_token}",
    }
    return client


@pytest.fixture
async def s3() -> S3:
    return S3(settings.aws.s3_bucket)


@pytest.fixture
async def sqs_example_worker_producer() -> SQSJobProducer:
    return SQSJobProducer(queue_url=settings.aws.sqs.example_worker.url + "-test")


@pytest.fixture
async def sqs_consumer(
    example_worker_repository: ExampleWorkerRepository,
) -> SQSConsumer:
    example_worker_processor = ExampleWorkerProcessor()
    example_worker_processor.repository = example_worker_repository
    return SQSConsumer(
        queue_url=settings.aws.sqs.example_worker.url + "-test",
        processors=[example_worker_processor],
    )

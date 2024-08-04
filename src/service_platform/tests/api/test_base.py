from typing import Any, AsyncGenerator
import unittest
from unittest.mock import Mock, patch

from faker import Faker
from fastapi import FastAPI, UploadFile
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncTransaction,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from service_platform.api.application import get_app, get_updated_app
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
from dishka.integrations.fastapi import setup_dishka

fake = Faker()

DEFAULT_USER_NAME = fake.user_name()
DEFAULT_USER_EMAIL = fake.email()
DEFAULT_USER_ID = fake.uuid4()
DEFAULT_USER_PICTURE = fake.image_url()

class BaseTestClass(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = await self._engine()
        await self.dbConnection(self.engine)
        # self.trans = await self.dbTransaction(self.connection)
        # self.session = await self.dbSession(self.connection)
        self.api = self.api(self.session)
        self.client = await self.client(self.api)
        
    async def _engine(self) -> AsyncEngine:
        """
        Create engine and databases.

        :yield: new engine.
        """
        return create_async_engine(str(settings.postgres_url))

    async def dbConnection(
        self,
        _engine: AsyncEngine,
    ) -> None:
        self.connection = await _engine.connect()
        self.trans = await self.connection.begin()

        session_maker = async_sessionmaker(
            self.connection,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.session = session_maker()
    
    async def dbTransaction(
        self,
        connection: AsyncConnection,
    ) -> AsyncTransaction:
        return connection.begin()
    
    async def dbSession(
        self,
        connection: AsyncConnection,
    ) -> AsyncSession:
        session_maker = async_sessionmaker(
            connection,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        return session_maker()
    
    def api(
        self,
        dbsession: AsyncSession,
    ) -> FastAPI:
        """
        Fixture for creating FastAPI app.

        :return: fastapi app with mocked dependencies.
        """
        application = get_updated_app()
        application.dependency_overrides[get_db_session] = lambda: dbsession
        return application  # noqa: WPS331
    
    async def client(
        self,
        api: FastAPI
    ) -> AsyncClient:
        """
        Fixture that creates client for requesting server.

        :param fastapi_app: the application.
        :yield: client for the app.
        """
        return  AsyncClient(transport=ASGITransport(app=api), base_url="http://test")
    
    # async def setUp(self) -> None:
    #     self.api = get_app()
    #     self.api.dependency_overrides[get_db_session] = lambda: self.session

    #     self.client = AsyncClient(app=self.api, base_url="http://test")
    #     self.user_repository = UserRepository(self.session)
    #     self.refresh_token_repository = RefreshTokenRepository(self.session)
    #     self.example_worker_repository = ExampleWorkerRepository()
    #     self.example_worker_repository.database = self.session
    #     self.user_manager = UserManager(self.user_repository)

    #     # Prepare data for tests
    #     self.test_user = await self.user_repository.insert_user(
    #         auth_id=DEFAULT_USER_ID,
    #         email=DEFAULT_USER_EMAIL,
    #         name=DEFAULT_USER_NAME,
    #         picture_url=DEFAULT_USER_PICTURE,
    #         auth_provider=AuthProvider.GOOGLE,
    #     )
    #     self.claim_generator = JWTClaimGenerator(registered_claim=JWTRegisteredClaim())
    #     self.token_generator = JWTTokenGenerator(claim_generator=self.claim_generator)
    #     self.access_token = self.token_generator.generate_token(
    #         CustomAuthentication(user_id=str(self.test_user.id), roles=[self.test_user.roles])
    #     ).access_token
    #     self.refresh_token = await self.refresh_token_repository.create(
    #         RefreshTokenRequest(user_id=self.test_user.id)
    #     )
    #     self.refresh_token = self.token_generator.generate_token(
    #         CustomAuthentication(user_id=str(self.test_user.id), roles=[self.test_user.roles], jti=str(self.refresh_token.id))
    #     ).refresh_token


    async def asyncTearDown(self):
        await self.session.close()
        await self.trans.rollback()
        await self.connection.close()
        await self.engine.dispose()
        await self.client.aclose()
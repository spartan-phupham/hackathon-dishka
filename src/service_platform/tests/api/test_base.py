from typing import Any, AsyncGenerator
import unittest
from unittest.mock import Mock, patch

from faker import Faker
from fastapi import FastAPI, UploadFile
from httpx import ASGITransport, AsyncClient
from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncTransaction,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session
)
from sqlalchemy.sql import text

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
from sqlalchemy import MetaData


fake = Faker()

DEFAULT_USER_NAME = fake.user_name()
DEFAULT_USER_EMAIL = fake.email()
DEFAULT_USER_ID = fake.uuid4()
DEFAULT_USER_PICTURE = fake.image_url()

class BaseTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await self.dbConnection()
        self.api = self.api(self.session)

        self.claim_generator = JWTClaimGenerator(
            registered_claim=JWTRegisteredClaim(),
        )
        self.token_generator = self.token_generator(self.claim_generator)

        self.user_repository = UserRepository(self.session)
    
    async def asyncTearDown(self):
        await self.truncate_all_table()
        await self.session.close()
        await self.engine.dispose()

    async def dbConnection(
        self
    ) -> None:
        self.engine = create_async_engine(str(settings.postgres_url))
        self.session = async_scoped_session(
            async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            ),
            scopefunc=current_task,
        )()
    
    def api(
        self,
        dbsession: AsyncSession,
    ) -> FastAPI:
        application = get_updated_app()
        application.dependency_overrides[get_db_session] = lambda: dbsession
        return application
    
    async def client(
        self,
        api: FastAPI
    ) -> AsyncClient:
        return  AsyncClient(transport=ASGITransport(app=api), base_url="http://test")
    
    def token_generator(
        self,
        claim_generator: JWTClaimGenerator,
    ) -> JWTTokenGenerator:
        return JWTTokenGenerator(
            claim_generator=claim_generator,
        )
    
    async def access_token(
        self,
        test_user: UserEntity
    ) -> str:
        """
        Fixture to create an access token for the test user.
        """
        authentication = CustomAuthentication(
            user_id=str(test_user.id),
            roles=[test_user.roles],
        )
        jwt_token = self.token_generator.generate_token(authentication)
        return jwt_token.access_token
    
    async def create_user(
        self,
        user_repository: UserRepository,
    ) -> UserEntity:
        return await user_repository.insert_user(
            auth_id=DEFAULT_USER_ID,
            email=DEFAULT_USER_EMAIL,
            name=DEFAULT_USER_NAME,
            picture_url=DEFAULT_USER_ID,
            auth_provider=AuthProvider.GOOGLE,
        )
    
    # async def setUp(self) -> None:

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

    async def truncate_all_table(self):
        excluded_tables = {
            "geography_columns",
            "geometry_columns",
            "spatial_ref_sys",
            "schema_version"
        }

        async with self.session as session:
            result = await session.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
            ))
            tables = [row[0] for row in result.fetchall() if row[0] not in excluded_tables]
                
            for table in tables:
                await session.execute(text(f"TRUNCATE {table}"))      
            await session.commit()
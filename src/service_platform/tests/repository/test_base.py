from typing import Any, AsyncGenerator
import unittest
from unittest.mock import Mock, patch

from faker import Faker
from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session
)
from sqlalchemy.sql import text

from service_platform.api.application import get_updated_app
from service_platform.client.model.auth_provider import AuthProvider
from service_platform.db.refresh_token.repository import RefreshTokenRepository
from service_platform.db.user.repository import UserRepository
from service_platform.db.user.table import UserEntity
from service_platform.service.postgres.dependency import get_db_session
from service_platform.settings import settings

fake = Faker()

DEFAULT_USER_NAME = fake.user_name()
DEFAULT_USER_EMAIL = fake.email()
DEFAULT_USER_ID = fake.uuid4()
DEFAULT_USER_PICTURE = fake.image_url()

class TestBase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await self.dbConnection()

        self.user_repository = UserRepository(self.session)
        self.refresh_token_repository = RefreshTokenRepository(self.session)
    
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
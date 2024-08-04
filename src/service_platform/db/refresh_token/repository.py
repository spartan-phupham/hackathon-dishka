import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from service_platform.core.repository.repository_base import BaseRepository
from service_platform.db.refresh_token.table import RefreshTokenEntity
from service_platform.service.postgres.dependency import get_db_session


class RefreshTokenRepository(BaseRepository[RefreshTokenEntity]):
    entity = RefreshTokenEntity

    def __init__(self, database: AsyncSession):
        super().__init__(database)
        self.database = database

    async def get_by_user_id(self, user_id: str) -> Optional[RefreshTokenEntity]:
        return await self.get_first([self.entity.id == user_id])

    async def find_first(
        self, user_id: uuid.UUID, jti: uuid.UUID, raise_error_if_not_found: bool = False
    ) -> Optional[RefreshTokenEntity]:
        return await self.get_first(
            conditions=[
                self.entity.user_id == user_id,
                self.entity.id == jti,
            ],
            raise_error_if_not_found=raise_error_if_not_found,
        )

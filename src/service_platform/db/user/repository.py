import uuid
from datetime import datetime, UTC

from sqlalchemy import and_

from service_platform.client.model.auth_provider import AuthProvider
from service_platform.client.model.user_role import UserRole
from service_platform.client.request.user.user_request import (
    CreateUserRequest,
    LoginUserRequest,
)
from service_platform.core.repository.repository_base import BaseRepository
from service_platform.db.user.table import UserEntity


class UserRepository(BaseRepository[UserEntity]):
    entity = UserEntity

    async def insert_user(
        self,
        auth_id: str,
        email: str,
        name: str,
        picture_url: str,
        auth_provider: AuthProvider,
    ) -> UserEntity:
        return await self.create(
            CreateUserRequest(
                email=email,
                name=name,
                roles=UserRole.USER,
                picture_url=picture_url,
                auth_id=auth_id,
                auth_provider=auth_provider.value,
            )
        )

    async def find_by_auth_id_and_auth_provider(
        self,
        auth_id: str,
        auth_provider: AuthProvider,
    ) -> UserEntity:
        condition = and_(
            self.entity.auth_provider == auth_provider.value,
            self.entity.auth_id == auth_id,
        )
        return await self.get_first(condition)

    async def update_user(
        self,
        user_id: uuid.UUID,
    ) -> UserEntity:
        return await self.update(
            LoginUserRequest(logged_in_at=datetime.now(UTC)), user_id
        )

    async def find_first(
        self,
        user_id: uuid.UUID,
    ) -> UserEntity:
        return await self.get_first([self.entity.id == user_id])

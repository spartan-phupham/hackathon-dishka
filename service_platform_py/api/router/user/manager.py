import uuid

from fastapi import Depends

from service_platform_py.api.router.user.schema import (
    DeletedUserResponse,
    UserResponse,
    CreateUserRequest,
    CreateUserResponse,
)
from service_platform_py.db.user.repository import UserRepository
from service_platform_py.db.user.table import UserEntity


class UserManager:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    @staticmethod
    async def sample() -> UserResponse:
        return UserResponse(
            id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            phone="+1234567890",
            email="chan@c0x12c.com",
            status="active",
            level="admin",
        )

    async def by_id(
        self,
        user_id: str,
    ) -> UserResponse:
        user: UserEntity = await self.user_repository.get(user_id)
        return self.__to_user_response(user)

    async def add_user(self, user: CreateUserRequest) -> CreateUserResponse:
        user: UserEntity = await self.user_repository.create(user)
        return CreateUserResponse(msg="Create user successfully", id=user.id)

    async def by_email(self, email: str) -> UserResponse:
        user: UserEntity = await self.user_repository.find(
            [UserEntity.email == email],
        )

        return self.__to_user_response(user)

    async def get_users(self, limit: int, skip: int) -> list[UserResponse]:
        users = await self.user_repository.get_multi(
            limit=limit,
            skip=skip,
        )
        return [self.__to_user_response(user) for user in users]

    async def remove(self, user_id: str) -> DeletedUserResponse:
        user: UserEntity = await self.user_repository.remove(user_id)
        return DeletedUserResponse(msg="Deleted user successfully", id=user.id)

    @staticmethod
    def __to_user_response(user: UserEntity) -> UserResponse:
        return UserResponse(
            id=user.id,
            phone=user.phone,
            email=user.email,
            status=user.status,
            level=user.level,
        )

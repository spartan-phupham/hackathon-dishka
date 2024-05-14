from fastapi import APIRouter, Depends, Body

from service_platform_py.api.router.user.manager import UserManager
from service_platform_py.api.router.user.schema import (
    DeletedUserResponse,
    UserResponse,
    CreateUserRequest,
    CreateUserResponse,
)
from service_platform_py.core.class_router import class_router

router = APIRouter()


@class_router(router)
class UserRouter:
    def __init__(self, user_manager: UserManager = Depends()):
        self.manager = user_manager

    @router.get("/sample")
    async def sample(self) -> UserResponse:
        return await self.manager.sample()

    @router.get("/by-id")
    async def by_id(
        self,
        user_id: str,
    ) -> UserResponse:
        return await self.manager.by_id(user_id)

    @router.post("/new")
    async def new(
        self,
        payload: CreateUserRequest = Body(CreateUserRequest),
    ) -> CreateUserResponse:
        return await self.manager.add_user(payload)

    @router.get("/")
    async def get_users(
        self,
        limit: int = 10,
        skip: int = 0,
    ) -> list[UserResponse]:
        return await self.manager.get_users(limit, skip)

    @router.delete("/")
    async def remove_user(
        self,
        user_id: str,
    ) -> DeletedUserResponse:
        return await self.manager.remove(user_id)

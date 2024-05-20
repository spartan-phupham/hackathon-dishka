from uuid import UUID

from fastapi import APIRouter, Depends, Body
from starlette.requests import Request

from service_platform_py.api.router.user.manager import UserManager
from service_platform_py.api.router.user.schema import (
    DeletedUserResponse,
    UpdateUserRequest,
    UserResponse,
    CreateUserRequest,
    CreateUserResponse,
)
from service_platform_py.core.authorization.base_permission import PermissionsDependency
from service_platform_py.core.authorization.is_authenticated import IsAuthenticated
from service_platform_py.core.class_router import class_router

router = APIRouter()


@class_router(router)
class UserRouter:
    def __init__(self, user_manager: UserManager = Depends()):
        self.manager = user_manager

    @router.get(
        "/current",
        dependencies=[
            Depends(PermissionsDependency([IsAuthenticated])),
        ],
    )
    async def current(
        self,
        request: Request,
    ) -> UserResponse:
        user = request.user
        return await self.manager.by_id(user.id)

    @router.get(
        "/by-id",
    )
    async def by_id(
        self,
        user_id: UUID,
    ) -> UserResponse:
        return await self.manager.by_id(user_id)

    @router.post("/new")
    async def new(
        self,
        payload: CreateUserRequest = Body(CreateUserRequest),
    ) -> CreateUserResponse:
        return await self.manager.add_user(payload)

    @router.put("/update")
    async def update_user(
        self,
        user_id: UUID,
        payload: UpdateUserRequest = Body(UpdateUserRequest),
    ) -> UserResponse:
        return await self.manager.update_user_status(payload, user_id)

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
        user_id: UUID,
    ) -> DeletedUserResponse:
        return await self.manager.remove(user_id)

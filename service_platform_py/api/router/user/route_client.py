from fastapi import APIRouter

from service_platform_py.api.router.user.schema import UserResponse
from service_platform_py.client.user.client import UserClient
from service_platform_py.core.class_router import class_router

router = APIRouter()


@class_router(router)
class UserClientRouter:
    def __init__(self):
        self.client = UserClient()

    @router.get("/by-id")
    async def by_id(
        self,
        user_id: str,
    ) -> UserResponse:
        return await self.client.by_id(user_id)

    @router.get("/")
    async def get_users(
        self,
        limit: int = 10,
        skip: int = 0,
    ) -> list[UserResponse]:
        return await self.client.get_users(limit, skip)

    @router.get("/notfound")
    async def get_not_found(
        self,
    ):
        import uuid

        return await self.client.by_id(uuid.uuid4())

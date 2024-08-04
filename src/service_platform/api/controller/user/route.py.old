from typing import Annotated

from fastapi import APIRouter, Depends

from service_platform.api.manager.user.manager import UserManager
from service_platform.client.response.user.user_response import UserResponse
from service_platform.core.class_router import class_router
from service_platform.core.middleware.authentication import (
    get_token_data,
)
from service_platform.core.security.model import TokenData

router = APIRouter()


@class_router(router)
class UserRouter:
    def __init__(self, user_manager: UserManager = Depends()):
        self.manager = user_manager

    @router.get("/me")
    async def me(
        self,
        token_data: Annotated[TokenData, Depends(get_token_data)],
    ) -> UserResponse:
        return await self.manager.me(user_id=token_data.user_id)

import logging

from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from service_platform.api.manager.user.manager import UserManager
from service_platform.client.response.user.user_response import UserResponse
from service_platform.core.middleware.authentication import get_token_data
from service_platform.core.security.model import TokenData

router = APIRouter()

@router.get("/me")
@inject
async def me(
    token_data: Annotated[TokenData, Depends(get_token_data)],
    manager: FromDishka[UserManager],
) -> UserResponse:
    return await manager.me(user_id=token_data.user_id)

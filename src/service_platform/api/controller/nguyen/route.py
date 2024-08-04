import uuid
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from service_platform.api.manager.health.manager import HealthManager
from service_platform.api.manager.user.manager import UserManager
from service_platform.client.response.user.user_response import UserResponse
from service_platform.core.middleware.authentication import public_endpoint


route = APIRouter()

@route.get("/")
@public_endpoint
@inject
async def index(manager: FromDishka[HealthManager]) -> str:
    return await manager.get_heath()

@route.get("/user")
@public_endpoint
@inject
async def index(manager: FromDishka[UserManager]) -> UserResponse:
    return await manager.me(uuid.UUID("deb8b3b5-c276-4904-885d-a097cafa20c0"))

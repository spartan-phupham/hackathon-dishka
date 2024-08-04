from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from service_platform.api.manager.health.manager import HealthManager
from service_platform.core.middleware.authentication import public_endpoint


route = APIRouter()

@route.get("/")
@public_endpoint
@inject
async def index(manager: FromDishka[HealthManager]) -> str:
    return await manager.get_heath()
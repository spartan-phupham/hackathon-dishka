from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject, DishkaRoute

from service_platform.api.manager.health.manager import HealthManager
from service_platform.core.class_router import class_router
from service_platform.core.middleware.authentication import public_endpoint

route = APIRouter(route_class=DishkaRoute)

@class_router(route)
class HealthRouter:
    @route.get("/")
    @public_endpoint
    async def index(self, manager: FromDishka[HealthManager]) -> str:
        return await manager.get_heath()
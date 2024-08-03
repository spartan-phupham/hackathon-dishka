from fastapi import APIRouter

from service_platform.api.controller.schema import MessageResponse
from service_platform.core.class_router import class_router
from service_platform.core.middleware.authentication import public_endpoint
from dishka.integrations.fastapi import FromDishka, inject, DishkaRoute

router = APIRouter(route_class=DishkaRoute)


@class_router(router)
class HealthRouter:
    @staticmethod
    @router.get("/")
    @public_endpoint
    async def health() -> MessageResponse:
        response = MessageResponse(message="OK")
        return response

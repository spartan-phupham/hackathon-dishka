from fastapi import APIRouter

from service_platform_py.api.router.health.schema import HealthResponse
from service_platform_py.core.class_router import class_router

router = APIRouter()


@class_router(router)
class HealthRouter:
    @staticmethod
    @router.get("/")
    async def health() -> HealthResponse:
        response = HealthResponse(message="OK")
        return response

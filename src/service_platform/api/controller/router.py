from fastapi.routing import APIRouter

from service_platform.api.controller.auth import auth_router
from service_platform.api.controller.health import health_router
from service_platform.api.controller.user import user_router

api_router = APIRouter()

# register all routers
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/user", tags=["user"])

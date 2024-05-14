from fastapi.routing import APIRouter

from service_platform_py.api.router.health import health_router
from service_platform_py.api.router.user import user_router

api_router = APIRouter()
# register all routers
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(user_router, prefix="/user", tags=["user"])

from contextlib import asynccontextmanager
from importlib import metadata

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import ORJSONResponse

from service_platform_py.api.auth_backend.auth_backend import AuthBackend
from service_platform_py.api.lifetime import (
    register_startup_event,
    register_shutdown_event,
)
from service_platform_py.api.router.router import api_router
from service_platform_py.core.auth.authentication import AuthenticationMiddleware
from service_platform_py.core.exception_handler import (
    request_validation_exception_handler,
    http_exception_handler,
    unicorn_exception_handler,
)
from service_platform_py.service.postgres.lifetime import (
    init_postgres,
    shutdown_postgres,
)
from service_platform_py.service.redis.lifetime import init_redis, shutdown_redis
from service_platform_py.settings import settings


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    # lifespan for app
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # on start up
        await register_startup_event()
        if settings.enable_redis:
            init_redis(app)
        if settings.enable_db:
            init_postgres(app)
        yield
        # on shutdown
        await register_shutdown_event()
        if settings.enable_redis:
            await shutdown_redis(app)
        if settings.enable_db:
            await shutdown_postgres(app)

    app = FastAPI(
        title="service_platform_py",
        version=metadata.version("service_platform_py"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        exception_handlers={
            RequestValidationError: request_validation_exception_handler,
            HTTPException: http_exception_handler,
            Exception: unicorn_exception_handler,
        },
        lifespan=lifespan,
    )
    if settings.enable_auth:
        app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app

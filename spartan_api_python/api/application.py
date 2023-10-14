from importlib import metadata

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import UJSONResponse

from spartan_api_python.api.lifecycle import Lifecycle
from spartan_api_python.api.router.router import api_router
from spartan_api_python.api.views.router import router
from spartan_api_python.core.exception_handler import (
    http_exception_handler,
    request_validation_exception_handler,
    unicorn_exception_handler,
)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="spartan_api_python",
        version=metadata.version("spartan_api_python"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )
    app.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler,
    )
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unicorn_exception_handler)

    # Adds startup and shutdown events.
    lifecycle = Lifecycle(app)
    lifecycle.register_startup_event()
    lifecycle.register_shutdown_event()

    # Main router for the API.
    app.include_router(router=router)
    app.include_router(router=api_router, prefix="/api")

    return app

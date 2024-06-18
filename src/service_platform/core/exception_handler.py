from fastapi.exceptions import HTTPException, RequestValidationError
from starlette import status
from starlette.requests import Request

from service_platform.core.response.app_response import AppResponse


async def http_exception_handler(request: Request, exc: HTTPException) -> AppResponse:
    """
    Exception handler for HTTPException.

    :param request: The request object.
    :param exc: The raised HTTPException.
    :return: An instance of AppResponse.
    """
    return AppResponse(
        status_code=exc.status_code,
        content=exc.detail,
        success=False,
    )


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> AppResponse:
    """
    Exception handler for RequestValidationError.

    :param request: The request object.
    :param exc: The raised RequestValidationError.
    :return: An instance of AppResponse.
    """
    return AppResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=exc.errors(),
        success=False,
    )


async def unicorn_exception_handler(request: Request, exc: Exception) -> AppResponse:
    """
    Exception handler for general Exception.

    :param request: The request object.
    :param exc: The raised Exception.
    :return: An instance of AppResponse.
    """
    return AppResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=f"{exc}",
        success=False,
    )

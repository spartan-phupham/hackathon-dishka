import json
import logging

from fastapi import HTTPException

from service_platform.exception.base_error import ClientException


class ErrorResponse:
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


async def exception_handler(request, exc):
    if isinstance(exc, ClientException):
        logging.error(f"Caught a client exception with error: {exc.message}")
        error_response = ErrorResponse(
            status_code=exc.code,
            message=exc.message,
        )
        raise HTTPException(
            status_code=exc.http_status_code,
            detail=json.loads(json.dumps(error_response.__dict__)),
        )
    logging.error(f"Caught an unhandled exception with error: {exc.detail}")
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.detail,
    )

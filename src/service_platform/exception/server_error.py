from http import HTTPStatus

from service_platform.exception.base_error import BaseError


class ServerError(BaseError):
    INTERNAL_SERVER_ERROR = BaseError(
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
        code=1000,
        message="The server cannot process the request for an unknown reason",
    )

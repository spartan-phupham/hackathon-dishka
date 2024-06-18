from http import HTTPStatus

from service_platform.exception.base_error import BaseError


class AuthError(BaseError):
    # AUTH

    INVALID_PROVIDER = BaseError(
        status=HTTPStatus.BAD_REQUEST,
        code=2011,
        message="Invalid Login Provider",
    )
    UNSUPPORTED_PROVIDER = BaseError(
        status=HTTPStatus.BAD_REQUEST,
        code=2012,
        message="Unsupported provider",
    )
    INVALID_CREDENTIALS = BaseError(
        status=HTTPStatus.UNAUTHORIZED,
        code=2013,
        message="Invalid Credentials",
    )
    INVALID_REFRESH_TOKEN = BaseError(
        status=HTTPStatus.UNAUTHORIZED,
        code=2014,
        message="Invalid Refresh Token",
    )

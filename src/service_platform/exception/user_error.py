from http import HTTPStatus

from service_platform.exception.base_error import BaseError
from service_platform.settings import settings


class UserError(BaseError):
    INVALID_PARAMETER = BaseError(
        status=HTTPStatus.BAD_REQUEST,
        code=2000,
        message="There is one or more parameter sent in invalid format or out of range",
    )
    USER_NOT_FOUND = BaseError(
        status=HTTPStatus.NOT_FOUND,
        code=2005,
        message="User not found",
    )
    UNAUTHORIZED = BaseError(
        status=HTTPStatus.UNAUTHORIZED,
        code=2010,
        message="Token is invalid",
    )

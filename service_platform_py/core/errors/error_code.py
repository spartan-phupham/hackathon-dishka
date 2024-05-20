from fastapi import HTTPException


NOT_FOUND = HTTPException(404, "Item not found")
KEY_EXISTS = HTTPException(422, "Key already exists")


class ServiceClientException(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(code, message)


class ForbiddenError(HTTPException):
    def __init__(
        self,
        detail: any = "User's permission denied",
        status_code: int = 403,
    ):
        """
        Generic Forbidden HTTP Exception with support for custom error code.

        :param error_code: Custom error code, unique throughout the app
        :param detail: detailed message of the error
        """
        super().__init__(
            status_code=status_code,
            detail=detail,
        )

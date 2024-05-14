from fastapi import HTTPException

NOT_FOUND = HTTPException(404, "Item not found")
KEY_EXISTS = HTTPException(422, "Key already exists")


class ServiceClientException(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(code, message)

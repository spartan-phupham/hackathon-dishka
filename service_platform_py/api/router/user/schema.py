import uuid

from service_platform_py.core.base_schema import CoreModel


class UserResponse(CoreModel):
    id: uuid.UUID
    email: str
    phone: str
    status: str
    level: str


class CreateUserRequest(CoreModel):
    email: str
    phone: str
    status: str = "active"
    level: str = "user"


class CreateUserResponse(CoreModel):
    msg: str
    id: uuid.UUID

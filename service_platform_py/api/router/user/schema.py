import uuid
from datetime import datetime

from service_platform_py.core.base_schema import CoreModel, OrmModel


# Same as Entity
class User(OrmModel):
    email: str
    phone: str
    status: str
    level: str
    logged_in_at: datetime | None


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


class UpdateUserRequest(CoreModel):
    status: str


class CreateUserResponse(CoreModel):
    msg: str
    id: uuid.UUID


class DeletedUserResponse(CreateUserResponse):
    pass

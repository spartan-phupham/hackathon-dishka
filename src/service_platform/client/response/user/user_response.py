import uuid
from datetime import datetime

from service_platform.core.base_schema import CoreModel


class UserResponse(CoreModel):
    id: uuid.UUID
    email: str
    name: str
    roles: list[str]
    picture_url: str | None
    created_at: datetime | None
    updated_at: datetime | None
    logged_in_at: datetime | None
    auth_provider: str | None

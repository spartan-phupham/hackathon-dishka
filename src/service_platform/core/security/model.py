import uuid

from service_platform.core.base_schema import CoreModel


class TokenData(CoreModel):
    user_id: uuid.UUID
    jti: uuid.UUID | None = None
    roles: list[str]

from datetime import datetime

from service_platform.client.model.auth_provider import AuthProvider
from service_platform.client.model.user_role import UserRole
from service_platform.core.base_schema import CoreModel


class CreateUserRequest(CoreModel):
    email: str
    name: str
    auth_id: str
    roles: str = UserRole.USER
    picture_url: str | None
    auth_provider: str = AuthProvider.GOOGLE.value


class LoginUserRequest(CoreModel):
    logged_in_at: datetime

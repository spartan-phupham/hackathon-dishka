import uuid

from service_platform.core.base_schema import CoreModel


class GoogleLoginRequest(CoreModel):
    access_token: str


class RefreshTokenRequest(CoreModel):
    user_id: uuid.UUID


class ProviderLoginRequest(CoreModel):
    code: str


class ProviderRequest(CoreModel):
    code: str


class CreateUserRequest(CoreModel):
    email: str
    name: str
    picture_url: str | None
    auth_id: str
    auth_provider: str

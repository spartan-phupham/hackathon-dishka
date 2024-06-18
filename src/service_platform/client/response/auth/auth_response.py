from service_platform.core.base_schema import CoreModel


class LoginResponse(CoreModel):
    roles: list[str]
    access_token: str
    refresh_token: str | None
    expires_in: int


class OauthUserResponse(CoreModel):
    id: str
    name: str | None = None
    email: str | None = None
    picture_url: str | None = None


class OauthExchangeCodeResponse(CoreModel):
    access_token: str | None = None
    expires_in: int | None = None


class OauthProviderUserResponse(CoreModel):
    sub: str | None = None
    name: str | None = None
    picture: str | None = None
    email: str | None = None

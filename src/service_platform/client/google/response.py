from service_platform.core.base_schema import CoreModel


class GoogleOauthTokenInfoResponse(CoreModel):
    aud: str | None = None
    sub: str | None = None
    expires_in: int | None = None
    email_verified: bool | None = None
    email: str | None = None

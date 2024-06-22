from service_platform.client.auth0.client import Auth0Client
from service_platform.client.response.auth.auth_response import (
    OauthUserResponse,
    OauthExchangeCodeResponse,
)
from service_platform.settings import settings, logger


class Auth0OAuthService:
    def __init__(self):
        self.client_id = settings.auth0.client_id
        self.client_secret = settings.auth0.client_secret
        self.redirect_uri = settings.auth0.redirect_uri
        self.base_url = settings.auth0.base_url
        self.client = Auth0Client()

    def get_redirect_uri(self) -> str:
        return (
            f"{self.base_url}/authorize?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope=openid%20profile%20email"
        )

    async def exchange_code_for_token(
        self, code: str
    ) -> OauthExchangeCodeResponse | None:
        try:
            data = {
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
            }

            token_info = await self.client.token_info(**data)
            return token_info
        except Exception as e:
            logger.error(f"Error exchange_code_for_token: {e}")
            return None

    async def get_user_info(self, access_token: str) -> OauthUserResponse | None:
        try:
            user_info = await self.client.user_info(access_token)
            return OauthUserResponse(
                id=user_info.sub,
                name=user_info.name,
                email=user_info.email,
                picture_url=user_info.picture,
            )
        except Exception as e:
            logger.error(f"Error get_user_info: {e}")
            return None

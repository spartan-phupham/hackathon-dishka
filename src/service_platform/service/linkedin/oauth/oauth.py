import secrets

from service_platform.client.linkedin.client import (
    LinkedinApiClient,
    LinkedinOauthClient,
)
from service_platform.client.response.auth.auth_response import (
    OauthUserResponse,
    OauthExchangeCodeResponse,
)
from service_platform.settings import settings, logger


class LinkedinOAuthService:
    def __init__(self) -> None:
        self.client_id = settings.linkedin.client_id
        self.client_secret = settings.linkedin.client_secret
        self.redirect_uri = settings.linkedin.redirect_uri
        self.oauth_client = LinkedinOauthClient()

    def get_redirect_uri(self) -> str:
        return (
            f"https://www.linkedin.com/oauth/v2/authorization?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope=openid%20profile%20email"
            f"&state={secrets.token_urlsafe(16)}"
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
            return await self.oauth_client.token_info(**data)
        except Exception as e:
            logger.error(f"Error exchange_code_for_token: {e}")
            return None

    @staticmethod
    async def get_user_info(access_token: str) -> OauthUserResponse | None:
        try:
            api_client = LinkedinApiClient(access_token)
            user_info = await api_client.user_info()
            return OauthUserResponse(
                id=user_info.sub,
                name=user_info.name,
                email=user_info.email,
                picture_url=user_info.picture,
            )
        except Exception as e:
            logger.error(f"Error get_user_info: {e}")
            return None

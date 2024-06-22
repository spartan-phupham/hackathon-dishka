from typing import List

from service_platform.client.google.client import GoogleApiClient, GoogleAccountClient
from service_platform.client.response.auth.auth_response import (
    OauthUserResponse,
    OauthExchangeCodeResponse,
)
from service_platform.settings import logger, settings


class GoogleOAuthService:
    def __init__(self) -> None:
        self.client_id = settings.google.client_id
        self.client_secret = settings.google.client_secret
        self.redirect_uri = settings.google.redirect_uri
        self.api_client = GoogleApiClient()
        self.account_client = GoogleAccountClient()

    @property
    def scopes(self) -> List[str]:
        return [
            "openid",
            "profile",
            "email",
        ]

    def get_redirect_uri(self) -> str:
        return (
            f"https://accounts.google.com/o/oauth2/auth?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={'%20'.join(self.scopes)}"
            f"&access_type=offline"
            f"&prompt=consent"
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
            return await self.account_client.token_info(**data)
        except Exception as e:
            logger.error(f"Error exchange_code_for_token: {e}")
            return None

    async def get_user_info(self, access_token: str) -> OauthUserResponse | None:
        try:
            user_info = await self.api_client.user_info(access_token)
            return OauthUserResponse(
                id=user_info.sub,
                name=user_info.name,
                email=user_info.email,
                picture_url=user_info.picture,
            )
        except Exception as e:
            logger.error(f"Error get_user_info: {e}")
            return None

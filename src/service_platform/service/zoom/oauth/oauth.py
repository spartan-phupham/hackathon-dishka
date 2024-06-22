from typing import List

from service_platform.client.response.auth.auth_response import (
    OauthUserResponse,
    OauthExchangeCodeResponse,
)
from service_platform.client.zoom.client import ZoomApiClient, ZoomClient
from service_platform.settings import logger, settings


class ZoomOAuthService:
    def __init__(self) -> None:
        self.client_id = settings.zoom.client_id
        self.client_secret = settings.zoom.client_secret
        self.redirect_uri = settings.zoom.redirect_uri
        self.zoom_client = ZoomClient()
        self.api_client = ZoomApiClient()

    def get_redirect_uri(self) -> str:
        return (
            f"https://zoom.us/oauth/authorize?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
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
            return await self.zoom_client.token_info(**data)
        except Exception as e:
            logger.error(f"Error exchange_code_for_token: {e}")
            return None

    async def get_user_info(self, access_token: str) -> OauthUserResponse | None:
        try:
            user_info = await self.api_client.user_info(access_token=access_token)
            return OauthUserResponse(
                id=user_info.sub,
                name=user_info.name,
                email=user_info.email,
                picture_url=user_info.picture,
            )
        except Exception as e:
            logger.error(f"Error get_user_info: {e}")
            return None

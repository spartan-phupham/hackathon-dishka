import requests
from uplink import response_handler, returns, post, Field

from service_platform.client.base_client import (
    BaseClient,
    logging_error_response,
    raise_for_status,
)
from service_platform.client.response.auth.auth_response import (
    OauthExchangeCodeResponse,
    OauthProviderUserResponse,
)
from service_platform.settings import settings


@response_handler(raise_for_status)  # Raise service_platform exception
@response_handler(logging_error_response)  # Logging error when request to client
class ZoomApiClient(BaseClient):
    def __init__(self, **kwargs):
        self.base_url = settings.zoom.api_url
        super().__init__(**kwargs)

    @returns.json(OauthProviderUserResponse)
    async def user_info(self, access_token: str) -> OauthProviderUserResponse:
        """Retrieves Zoom user info by access_token"""
        bearer_headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{self.base_url}/v2/users/me"
        response = requests.get(url, headers=bearer_headers)
        data = response.json()
        return OauthProviderUserResponse(
            sub=data.get("id"),
            name=data.get("display_name"),
            picture=data.get("pic_url"),
            email=data.get("email"),
        )


@response_handler(raise_for_status)  # Raise service_platform exception
@response_handler(logging_error_response)  # Logging error when request to client
class ZoomClient(BaseClient):
    base_url = settings.zoom.zoom_url

    @returns.json(OauthExchangeCodeResponse)
    @post("/oauth/token")
    async def token_info(
        self,
        code: Field,
        client_id: Field,
        client_secret: Field,
        redirect_uri: Field,
        grant_type: Field = "authorization_code",
    ) -> OauthExchangeCodeResponse:
        """Retrieves zoom token info access_token"""
        pass

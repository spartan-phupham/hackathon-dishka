import requests
from uplink import get, response_handler, returns, Field, headers

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
class LinkedinOauthClient(BaseClient):
    base_url = settings.linkedin.oauth_url

    @returns.json(OauthExchangeCodeResponse)
    @headers({"Content-Type": "application/x-www-form-urlencoded"})
    @get("/oauth/v2/accessToken")
    async def token_info(
        self,
        code: Field,
        client_id: Field,
        client_secret: Field,
        redirect_uri: Field,
        grant_type: Field = "authorization_code",
    ) -> OauthExchangeCodeResponse:
        """Retrieves LinkedIn token info access_token"""
        pass


@response_handler(raise_for_status)  # Raise service_platform exception
@response_handler(logging_error_response)  # Logging error when request to client
class LinkedinApiClient(BaseClient):
    def __init__(self, access_token: str, **kwargs):
        self.base_url = settings.linkedin.api_url
        self.access_token = access_token
        super().__init__(**kwargs)

    @returns.json(OauthProviderUserResponse)
    async def user_info(self) -> OauthProviderUserResponse:
        """Retrieves LinkedIn user info by access_token"""
        bearer_headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.base_url}/v2/userinfo"
        response = requests.get(url, headers=bearer_headers)
        return OauthProviderUserResponse(**response.json())

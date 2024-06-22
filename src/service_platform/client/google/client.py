from uplink import get, Query, response_handler, returns, post, Field

from service_platform.client.base_client import (
    BaseClient,
    logging_error_response,
    raise_for_status,
)
from service_platform.client.response.auth.auth_response import (
    OauthProviderUserResponse,
    OauthExchangeCodeResponse,
)
from service_platform.settings import settings


@response_handler(raise_for_status)  # Raise service_platform exception
@response_handler(logging_error_response)  # Logging error when request to client
class GoogleApiClient(BaseClient):
    base_url = settings.google.api_url

    @returns.json(OauthProviderUserResponse)
    @get("/oauth2/v3/userinfo")
    async def user_info(
        self, access_token: Query("access_token")
    ) -> OauthProviderUserResponse:
        """Retrieves google user info by access_token"""
        pass


@response_handler(raise_for_status)  # Raise service_platform exception
@response_handler(logging_error_response)  # Logging error when request to client
class GoogleAccountClient(BaseClient):
    base_url = settings.google.oauth_url

    @returns.json(OauthExchangeCodeResponse)
    @post("/token")
    async def token_info(
        self,
        code: Field,
        client_id: Field,
        client_secret: Field,
        redirect_uri: Field,
        grant_type: Field = "authorization_code",
    ) -> OauthExchangeCodeResponse:
        """Retrieves google token info access_token"""
        pass

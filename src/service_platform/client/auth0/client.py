from uplink import get, Query, response_handler, returns, Field, post

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
class Auth0Client(BaseClient):
    base_url = settings.auth0.base_url

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
        pass

    @returns.json(OauthProviderUserResponse)
    @get("/userinfo")
    async def user_info(
        self, access_token: Query("access_token")
    ) -> OauthProviderUserResponse:
        pass

from uplink import get, Query, response_handler, returns

from service_platform_py.api.router.user.schema import UserResponse
from service_platform_py.client.base_client import (
    BaseClient,
    logging_error_response,
    raise_for_status,
)


@response_handler(raise_for_status)  # Raise service_platform_py exception
@response_handler(logging_error_response)  # Logging error when request to client
class UserClient(BaseClient):
    base_url = "http://0.0.0.0:8080"

    @returns.json(list[UserResponse])
    @get("/api/user/by-id")
    async def by_id(self, user_id: Query("user_id")) -> UserResponse:
        """Retrieves user by id"""
        pass

    @returns.json(list[UserResponse])
    @get("/api/user/")
    async def get_users(
        self,
        limit: Query("limit"),
        skip: Query("user_id"),
    ) -> list[UserResponse]:
        """Get all user"""
        pass

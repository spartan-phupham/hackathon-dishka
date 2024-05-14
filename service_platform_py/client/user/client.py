from uplink import Consumer, get, Query

from service_platform_py.api.router.user.schema import UserResponse


class UserClient(Consumer):

    @get("api/user/sample")
    def sample(self) -> UserResponse:
        """Retrieves a sample user"""

    @get("api/user/by-id")
    def by_id(self, user_id: Query("user_id")) -> UserResponse:
        """Retrieves user by id"""

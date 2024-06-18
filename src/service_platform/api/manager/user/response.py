from service_platform.client.response.user.user_response import UserResponse
from service_platform.db.user.table import UserEntity


class UserResponseConverter:
    def __init__(
        self,
    ):
        pass

    @staticmethod
    def to_user_response(user: UserEntity) -> UserResponse:
        return UserResponse(
            id=user.id,
            roles=[user.roles],
            email=user.email,
            name=user.name,
            picture_url=user.picture_url,
            created_at=user.created_at,
            updated_at=user.updated_at,
            logged_in_at=user.logged_in_at,
            auth_provider=user.auth_provider,
        )

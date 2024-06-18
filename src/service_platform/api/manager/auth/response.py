from service_platform.client.response.auth.auth_response import LoginResponse
from service_platform.db.user.table import UserEntity


class AuthResponseConverter:
    def __init__(
        self,
    ):
        pass

    @staticmethod
    def to_login_response(
        user: UserEntity,
        access_token: str,
        refresh_token: str = None,
        expires_in: int = None,
    ) -> LoginResponse:
        return LoginResponse(
            roles=[user.roles],
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )

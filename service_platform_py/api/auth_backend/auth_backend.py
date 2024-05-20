from typing import Optional, Tuple

from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.requests import HTTPConnection

from service_platform_py.db.user.repository import UserRepository
from service_platform_py.db.user.table import UserEntity


class AuthBackend(AuthenticationBackend):
    """
    Own Auth Backend based on Starlette's AuthenticationBackend.

    Use instance of this class as `backend` argument to `add_middleware` func:

    .. code-block:: python

        app = FastAPI()

        @app.on_event('startup')
        async def startup():
            app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

    """

    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> Tuple[bool, Optional[UserEntity]]:
        """
        Main function that AuthenticationMiddleware uses from this backend.
        Should return whether request is authenticated based on credentials and
        if it was, return also user instance.

        :param conn: HTTPConnection of the current request-response cycle
        :return: 2-tuple: is authenticated & user instance if exists
        """
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, None
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise AuthenticationError("Not authenticated")
        if scheme.lower() != "bearer":
            raise AuthenticationError("Invalid authentication credentials")
        # Handle Logic of JWT key
        if credentials is None:
            return False, None

        session = conn.app.state.db_session_factory
        user_repo = UserRepository(session)
        user = await user_repo.get(obj_id=credentials)
        if user is None:
            return False, None
        # update login_at, using get_now func
        return True, user

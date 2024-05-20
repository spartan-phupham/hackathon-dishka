from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from service_platform_py.core.response.app_response import AppResponse


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    """
    Own Authentication Middleware based on Starlette's default one.

    Use instance of this class as a first argument to `add_middleware` func:

    .. code-block:: python

        app = FastAPI()

        @app.on_event('startup')
        async def startup():
            app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

    """

    @staticmethod
    def default_on_error(
        conn: HTTPConnection,
        exc: Exception,
    ) -> AppResponse:
        """
        Overriden method just to make sure we return response in our format.

        :param conn: HTTPConnection of the current request-response cycle
        :param exc: Any exception that could have been raised
        :return: Return with error data as dict and 403 status code
        """
        return AppResponse(
            content=str(exc),
            status_code=400,
            success=False,
        )

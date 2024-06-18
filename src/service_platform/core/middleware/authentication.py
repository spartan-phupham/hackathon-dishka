import re
from typing import Callable, Coroutine, Any, Annotated, Set

from fastapi import HTTPException, APIRouter, Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from yarl import URL

from service_platform.core.middleware.model import TokenType
from service_platform.core.security.jwt_token_validator import JwtTokenValidator
from service_platform.core.security.model import TokenData
from service_platform.db.refresh_token.repository import RefreshTokenRepository
from service_platform.settings import logger

BEARER_SCHEME = HTTPBearer()


def get_token_data(
    request: Request, _: Annotated[HTTPAuthorizationCredentials, Depends(BEARER_SCHEME)]
) -> TokenData:
    token_data = getattr(request.state, "token_data", None)

    if not token_data:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return token_data


def error_response(error_msg: str, status_code: int) -> JSONResponse:
    logger.error(error_msg)
    return JSONResponse(
        content={"error": {"message": error_msg}},
        status_code=status_code,
    )


def public_endpoint(func: Callable):
    func.is_public = True
    return func


def include_public_paths(router: APIRouter, public_paths: set[URL]):
    for route in router.routes:
        if getattr(route.endpoint, "is_public", False):
            public_paths.add(
                URL(route.path[:-1] if route.path.endswith("/") else route.path)
            )


def refresh_token_endpoint(func: Callable):
    func.is_refresh = True
    return func


def include_refresh_token_paths(router: APIRouter, refresh_token_paths: Set[URL]):
    for route in router.routes:
        if getattr(route.endpoint, "is_refresh", False):
            refresh_token_paths.add(
                URL(route.path[:-1] if route.path.endswith("/") else route.path)
            )


def is_public_path(normalized_path: str, public_paths: Set[URL]) -> bool:
    for url in public_paths:
        pattern = convert_to_regex(url)
        if pattern.match(str(normalized_path)):
            return True
    return False


def convert_to_regex(url: URL):
    decoded_path = url.path
    # Convert %7B and %7D to {}
    decoded_path = decoded_path.replace("%7B", "{").replace("%7D", "}")
    # Escape other regex special characters
    decoded_path = re.escape(decoded_path)
    # Replace escaped { and } with regex patterns
    pattern = decoded_path.replace("\\{", "{").replace("\\}", "}")
    # Replace {placeholder} with regex to match alphanumeric characters
    pattern = pattern.replace("{", "(?P<").replace("}", ">[a-zA-Z0-9]+)")
    return re.compile(f"^{pattern}$")


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        public_paths: set[URL],
        refresh_token_paths: set[URL] = None,
        token_validator: JwtTokenValidator = JwtTokenValidator(),
        refresh_token_repository: RefreshTokenRepository = Depends(),
        **kwargs,
    ):
        super().__init__(app, **kwargs)
        self.token_validator = token_validator
        self.app = app
        self.public_paths = public_paths
        self.refresh_token_paths = refresh_token_paths
        self.refresh_token_repository = refresh_token_repository
        if self.refresh_token_paths is None:
            self.refresh_token_paths = set()

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[Any, Any, Response]],
    ) -> JSONResponse | Response:
        if request.url.path.startswith("/api"):
            normalized_path = request.url.path[len("/api") :]
            if normalized_path.endswith("/"):
                normalized_path = normalized_path[:-1]

            if is_public_path(
                normalized_path=normalized_path, public_paths=self.public_paths
            ):
                return await call_next(request)
            try:
                if request.method != "OPTIONS":
                    if "Authorization" not in request.headers:
                        return error_response("Unauthorized", 401)
                    token_header = request.headers["Authorization"]
                    if token_header.startswith("Bearer "):
                        token = token_header.split("Bearer ")[-1]
                        token_type = TokenType.access_token
                        if URL(normalized_path) in self.refresh_token_paths:
                            token_type = TokenType.refresh_token

                        token_data = await self.token_validator.validate(
                            token, token_type
                        )
                        if not token_data:
                            return error_response("Unauthorized", 401)

                        request.state.token_data = token_data
                    else:
                        return error_response("Token should begin with Bearer", 400)
            except Exception as e:
                return error_response(f"Token validation error: {e}", 400)
        return await call_next(request)

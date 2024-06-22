import uuid
from typing import Any

from fastapi import Depends

from service_platform.api.controller.schema import MessageResponse
from service_platform.api.manager.auth.response import AuthResponseConverter
from service_platform.client.model.auth_provider import AuthProvider
from service_platform.client.request.auth.auth_request import (
    ProviderLoginRequest,
    RefreshTokenRequest,
)
from service_platform.client.response.auth.auth_response import LoginResponse
from service_platform.core.response.app_response import Message
from service_platform.core.security.custom_authentication import CustomAuthentication
from service_platform.core.security.jwt_token_generator import JWTTokenGenerator
from service_platform.db.refresh_token.repository import RefreshTokenRepository
from service_platform.db.user.repository import UserRepository
from service_platform.exception.auth_error import AuthError
from service_platform.service.auth0.oauth import Auth0OAuthService
from service_platform.service.google.oauth import GoogleOAuthService
from service_platform.service.linkedin.oauth import LinkedinOAuthService
from service_platform.service.zoom.oauth import ZoomOAuthService


class AuthManager:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        google_auth: GoogleOAuthService = Depends(),
        linkedin_auth: LinkedinOAuthService = Depends(),
        zoom_auth: ZoomOAuthService = Depends(),
        auth0_auth: Auth0OAuthService = Depends(),
        token_generator: JWTTokenGenerator = Depends(),
        auth_response_converter: AuthResponseConverter = Depends(),
        refresh_token_repository: RefreshTokenRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.google_auth = google_auth
        self.linkedin_auth = linkedin_auth
        self.zoom_auth = zoom_auth
        self.auth0_auth = auth0_auth
        self.token_generator = token_generator
        self.auth_response_converter = auth_response_converter
        self.refresh_token_repository = refresh_token_repository

    def _init_provider_config(self, provider: AuthProvider) -> None:
        # Pass the init provider config if needed
        pass

    def _get_auth_method(self, provider: AuthProvider) -> Any:
        auth = getattr(self, f"{provider.value.lower()}_auth", None)
        if auth is None:
            raise AuthError.UNSUPPORTED_PROVIDER.as_http_exception(
                custom_message=f"Unsupported provider: {provider.value}"
            )
        return auth

    async def get_provider_redirect_url(
        self,
        provider: AuthProvider,
    ) -> MessageResponse:
        self._init_provider_config(provider=provider)
        auth_method = self._get_auth_method(provider=provider)
        return MessageResponse(message=auth_method.get_redirect_uri())

    async def _handle_login(
        self,
        auth_id: str,
        email: str,
        name: str,
        picture_url: str,
        auth_provider: AuthProvider,
    ) -> LoginResponse:
        user = await self.user_repository.find_by_auth_id_and_auth_provider(
            auth_id=auth_id,
            auth_provider=auth_provider,
        )
        if user is None:
            user = await self.user_repository.insert_user(
                auth_id=auth_id,
                email=email,
                name=name,
                picture_url=picture_url,
                auth_provider=auth_provider,
            )
        else:
            await self.user_repository.update_user(user.id)
        refresh_token = await self.refresh_token_repository.create(
            RefreshTokenRequest(user_id=user.id)
        )

        authentication = CustomAuthentication(
            user_id=str(user.id), roles=[user.roles], jti=str(refresh_token.id)
        )

        jwt_token = self.token_generator.generate_token(authentication)

        return self.auth_response_converter.to_login_response(
            user=user,
            access_token=jwt_token.access_token,
            refresh_token=jwt_token.refresh_token,
            expires_in=jwt_token.expires_in,
        )

    async def provider_authorize_login(
        self,
        payload: ProviderLoginRequest,
        provider: AuthProvider,
    ) -> LoginResponse | None:
        self._init_provider_config(provider=provider)

        auth_method = self._get_auth_method(provider=provider)
        if payload.code is not None:
            token_info = await auth_method.exchange_code_for_token(code=payload.code)
            if token_info is None:
                raise AuthError.INVALID_CREDENTIALS.as_http_exception()
            user_info = await auth_method.get_user_info(token_info.access_token)
            if user_info is None:
                raise AuthError.INVALID_CREDENTIALS.as_http_exception()
            return await self._handle_login(
                auth_id=user_info.id,
                email=user_info.email,
                name=user_info.name,
                picture_url=user_info.picture_url,
                auth_provider=provider,
            )
        else:
            raise AuthError.INVALID_CREDENTIALS.as_http_exception()

    async def refresh_access_token(
        self, user_id: uuid.UUID, jti: uuid.UUID
    ) -> LoginResponse:
        user = await self.user_repository.find_first(user_id)
        if user is None:
            raise AuthError.INVALID_REFRESH_TOKEN.as_http_exception()

        authentication = CustomAuthentication(
            user_id=str(user.id),
            roles=[user.roles],
            jti=str(jti),
        )
        refresh_token = await self.refresh_token_repository.find_first(
            user_id=user.id, jti=jti
        )
        if refresh_token is None:
            raise AuthError.INVALID_REFRESH_TOKEN.as_http_exception()

        jwt_token = self.token_generator.generate_token(
            authentication, generate_refresh_token=False
        )

        return self.auth_response_converter.to_login_response(
            user=user,
            access_token=jwt_token.access_token,
            expires_in=jwt_token.expires_in,
        )

    async def logout(self, user_id: uuid.UUID, jti: uuid.UUID) -> MessageResponse:
        user = await self.user_repository.find_first(user_id)
        if user is None:
            raise AuthError.INVALID_REFRESH_TOKEN.as_http_exception()

        await self.refresh_token_repository.remove(jti)
        return MessageResponse(message=Message.LOGGED_OUT)

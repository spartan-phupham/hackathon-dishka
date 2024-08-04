from dishka import Provider, Scope, provide

from typing import AsyncGenerator
from service_platform.api.manager.auth.response import AuthResponseConverter
from service_platform.api.manager.user.response import UserResponseConverter
from service_platform.core.security.jwt_claim_generator import JWTClaimGenerator
from service_platform.core.security.jwt_registered_claim import JWTRegisteredClaim
from service_platform.core.security.jwt_token_generator import JWTTokenGenerator
from service_platform.service.auth0.oauth.oauth import Auth0OAuthService
from service_platform.service.google.oauth.oauth import GoogleOAuthService
from service_platform.service.linkedin.oauth.oauth import LinkedinOAuthService
from service_platform.service.zoom.oauth.oauth import ZoomOAuthService

from service_platform.settings import settings

from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)


class CoreFactory(Provider):
    component = "Core"
    def __init__(self) -> None:
        super().__init__()
        pass

    @provide(scope=Scope.APP)
    def provide_google_oauth_service(self) -> GoogleOAuthService:
        return GoogleOAuthService()

    @provide(scope=Scope.APP)
    def provide_linkedin_oauth_service(self) -> LinkedinOAuthService:
        return LinkedinOAuthService()

    @provide(scope=Scope.APP)
    def provide_zoom_oauth_service(self) -> ZoomOAuthService:
        return ZoomOAuthService()
    
    @provide(scope=Scope.APP)
    def provide_auth0_oauth_service(self) -> Auth0OAuthService:
        return Auth0OAuthService()

    @provide(scope=Scope.APP)
    def provide_jwt_token_generator(self) -> JWTTokenGenerator:
        registered_claim = JWTRegisteredClaim()
        jwt_claim_generator = JWTClaimGenerator(registered_claim)
        return JWTTokenGenerator(jwt_claim_generator)

    @provide(scope=Scope.APP)
    def provide_auth_response_converter(self) -> AuthResponseConverter:
        return AuthResponseConverter()

    @provide(scope=Scope.APP)
    def provide_user_response_converter(self) -> UserResponseConverter:
        return UserResponseConverter()
    
    
    @provide(scope=Scope.REQUEST)
    async def provide_db_session_factory(self) -> AsyncGenerator[AsyncSession, None]:
        engine = create_async_engine(str(settings.postgres_url))
        session = async_scoped_session(
            async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
            ),
            scopefunc=current_task,
        )()
        print("Provide database session")
        
        yield session

        await session.commit()
        await session.close()

        print("Successfully close DB session")

from typing import Annotated
from service_platform.api.manager.auth.manager import AuthManager
from service_platform.api.manager.auth.response import AuthResponseConverter
from service_platform.api.manager.health.manager import HealthManager
from service_platform.api.manager.user.manager import UserManager
from dishka import Provider, Scope, provide, FromComponent

from service_platform.api.manager.user.response import UserResponseConverter
from service_platform.core.security.jwt_token_generator import JWTTokenGenerator
from service_platform.db.refresh_token.repository import RefreshTokenRepository
from service_platform.db.user.repository import UserRepository
from service_platform.service.auth0.oauth.oauth import Auth0OAuthService
from service_platform.service.google.oauth.oauth import GoogleOAuthService
from service_platform.service.linkedin.oauth.oauth import LinkedinOAuthService
from service_platform.service.zoom.oauth.oauth import ZoomOAuthService
class ManagerFactory(Provider):
    def __init__(self) -> None:
        super().__init__()
        pass

    @provide(scope=Scope.APP)
    def provide_health_manager(self) -> HealthManager:
        print("This provider is called, should be called 1 time. Will be called multiple times if Scope.REQUEST")
        return HealthManager()
    
    @provide(scope=Scope.REQUEST)
    def provide_auth_manager(
        self,
        user_repository: Annotated[UserRepository, FromComponent("Database")],
        refresh_token_repository: Annotated[RefreshTokenRepository, FromComponent("Database")],
        google_auth: Annotated[GoogleOAuthService, FromComponent("Core")],
        linkedin_auth: Annotated[LinkedinOAuthService, FromComponent("Core")],
        zoom_auth: Annotated[ZoomOAuthService, FromComponent("Core")],
        auth0_auth: Annotated[Auth0OAuthService, FromComponent("Core")],
        token_generator: Annotated[JWTTokenGenerator, FromComponent("Core")],
        auth_response_converter: Annotated[AuthResponseConverter, FromComponent("Core")]
        
    ) -> AuthManager:
        return AuthManager(
            user_repository=user_repository,
            refresh_token_repository=refresh_token_repository,
            google_auth=google_auth,
            linkedin_auth=linkedin_auth,
            zoom_auth=zoom_auth,
            auth0_auth=auth0_auth,
            token_generator=token_generator,
            auth_response_converter=auth_response_converter
        )
    
    @provide(scope=Scope.REQUEST)
    def provide_user_manager(
        self,
        user_repository: Annotated[UserRepository, FromComponent("Database")],
        user_response_converter: Annotated[UserResponseConverter, FromComponent("Core")]
    ) -> UserManager:
        return UserManager(
            user_repository=user_repository,
            user_response_converter=user_response_converter
        )




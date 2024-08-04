from dishka import Provider, Scope, provide

from service_platform.core.security.jwt_token_generator import JWTTokenGenerator
from service_platform.service.auth0.oauth.oauth import Auth0OAuthService
from service_platform.service.google.oauth.oauth import GoogleOAuthService
from service_platform.service.linkedin.oauth.oauth import LinkedinOAuthService
from service_platform.service.zoom.oauth.oauth import ZoomOAuthService


class CoreFactory(Provider):
    component = "Core"
    def __init__(self) -> None:
        super().__init__()
        pass

    @provide(scope=Scope.APP)
    def provide_google_oauth_service(self):
        return GoogleOAuthService()

    @provide(scope=Scope.APP)
    def provide_linkedin_oauth_service(self):
        return LinkedinOAuthService()

    @provide(scope=Scope.APP)
    def provide_zoom_oauth_service(self):
        return ZoomOAuthService()
    
    @provide(scope=Scope.APP)
    def provide_auth0_oauth_service(self):
        return Auth0OAuthService()
    
    @provide(scope=Scope.APP)
    def provide_jwt_token_generator(self):
        return JWTTokenGenerator()
    

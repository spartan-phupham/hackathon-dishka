from typing import Annotated
from service_platform.api.manager.auth.manager import AuthManager
from service_platform.api.manager.health.manager import HealthManager
from service_platform.api.manager.user.manager import UserManager
from dishka import Provider, Scope, provide, FromComponent

from service_platform.db.refresh_token.repository import RefreshTokenRepository
from service_platform.db.user.repository import UserRepository

class ManagerFactory(Provider):
    def __init__(self) -> None:
        super().__init__()
        pass

    @provide(scope=Scope.APP)
    def provide_health_manager(self) -> HealthManager:
        print("This provider is called, should be called 1 time. Will be called multiple times if Scope.REQUEST")
        return HealthManager()
    
    @provide(scope=Scope.APP)
    def provide_auth_manager(
        self,
        user_repository: Annotated[UserRepository, FromComponent("Database")],
        refresh_token_repository: Annotated[RefreshTokenRepository, FromComponent("Database")],
        
    ) -> AuthManager:
        return AuthManager()
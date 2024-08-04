from dishka import Provider, Scope, provide

from service_platform.db.refresh_token.repository import RefreshTokenRepository
from service_platform.db.user.repository import UserRepository


class DatabaseFactory(Provider):
    def __init__(self) -> None:
        super().__init__()

    component = "Database"

    @provide(scope=Scope.APP)
    def provide_user_repository(self) -> UserRepository:
        return UserRepository()

    @provide(scope=Scope.APP)
    def provide_refresh_token_reopsitory(self) -> RefreshTokenRepository:
        return RefreshTokenRepository()
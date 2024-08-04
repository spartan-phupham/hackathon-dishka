from typing import Annotated
from dishka import FromComponent, Provider, Scope, provide

from service_platform.db.refresh_token.repository import RefreshTokenRepository
from service_platform.db.user.repository import UserRepository

from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseFactory(Provider):
    component = "Database"
    
    def __init__(self) -> None:
        super().__init__()

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(
        self,
        database: Annotated[AsyncSession, FromComponent("Core")]
    ) -> UserRepository:
        return UserRepository(database=database)

    @provide(scope=Scope.REQUEST)
    def provide_refresh_token_reopsitory(
        self,
        database: Annotated[AsyncSession, FromComponent("Core")]
    ) -> RefreshTokenRepository:
        return RefreshTokenRepository(database=database)
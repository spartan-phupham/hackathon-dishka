from service_platform.api.manager.auth.manager import AuthManager
from service_platform.api.manager.health.manager import HealthManager
from service_platform.api.manager.user.manager import UserManager
from dishka import Provider, Scope, provide

class ManagerFactory(Provider):
    def __init__(self) -> None:
        super().__init__()
        pass

    @provide(scope=Scope.RUNTIME)
    def provide_health_manager(self) -> HealthManager:
        print("This provider is called, should be called 1 time. Will be called multiple times if Scope.REQUEST")
        return HealthManager()
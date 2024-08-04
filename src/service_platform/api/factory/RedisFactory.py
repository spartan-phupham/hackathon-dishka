from typing import Iterable
from dishka import Provider, Scope, provide
from redis import ConnectionPool

from service_platform.settings import settings


class RedisFactory(Provider): 
    component = "Redis"
    
    def __init__(self) -> None:
        super().__init__()
        pass

    @provide(scope=Scope.APP)
    def provide_redis(self) -> Iterable[ConnectionPool]:
        conn = ConnectionPool.from_url(str(settings.redis_url))
        print("Initialize redis")
        yield conn
        conn.disconnect()
        print("Disconnect redis")

        

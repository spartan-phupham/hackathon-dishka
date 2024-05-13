import taskiq_fastapi
from taskiq import InMemoryBroker
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from service_platform_py.settings import settings

result_backend = RedisAsyncResultBackend(
    redis_url=str(settings.redis_url),
)
broker = ListQueueBroker(
    str(settings.redis_url),
).with_result_backend(result_backend)

if settings.environment.lower() == "test":
    broker = InMemoryBroker()

taskiq_fastapi.init(
    broker,
    "service_platform_py.api.application:get_app",
)

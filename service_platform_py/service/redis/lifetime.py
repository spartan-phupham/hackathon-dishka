from fastapi import FastAPI
from redis.asyncio import ConnectionPool

from service_platform_py.settings import settings, logger


def init_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection pool for redis.

    :param app: current fastapi application.
    """
    app.state.redis_pool = ConnectionPool.from_url(
        str(settings.redis_url),
    )
    logger.info(f"redis connect: {app.state.redis_pool.can_get_connection()}")


async def shutdown_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    Closes redis connection pool.

    :param app: current FastAPI app.
    """
    await app.state.redis_pool.disconnect()
    logger.info("redis disconnected")

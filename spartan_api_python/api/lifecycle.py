from typing import Awaitable, Callable

from fastapi import FastAPI

from spartan_api_python.service.redis.lifetime import init_redis, shutdown_redis
from spartan_api_python.tkq import broker


class Lifecycle:

    def __init__(self, app: FastAPI):
        self.app = app

    def register_startup_event(self) -> Callable[[], Awaitable[None]]:  # pragma: no cover
        """
        Actions to run on application startup.
        This function uses fastAPI app to store data
        in the state, such as db_engine.
        :return: function that actually performs actions.
        """

        @self.app.on_event("startup")
        async def _startup() -> None:  # noqa: WPS430
            if not broker.is_worker_process:
                await broker.startup()

        init_redis(self.app)
        return _startup

    def register_shutdown_event(self) -> Callable[[], Awaitable[None]]:  # pragma: no cover
        """
        Actions to run on application's shutdown.
        :return: function that actually performs actions.
        """

        @self.app.on_event("shutdown")
        async def _shutdown() -> None:  # noqa: WPS430
            if not broker.is_worker_process:
                await broker.shutdown()

            await shutdown_redis(self.app)

        return _shutdown

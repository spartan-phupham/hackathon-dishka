from asyncio import current_task

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from service_platform_py.settings import settings, logger


def init_postgres(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection for postgres.

    :param app: current fastapi application.
    """
    engine = create_async_engine(str(settings.postgres_url))
    session_factory = async_scoped_session(
        async_sessionmaker(
            engine,
            expire_on_commit=False,
        ),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
    logger.info("postgres initialized")


async def shutdown_postgres(app: FastAPI) -> None:  # pragma: no cover
    """
    Closes postgres connectio.

    :param app: current FastAPI app.
    """
    await app.state.db_engine.dispose()
    logger.info("postgres disconnected")

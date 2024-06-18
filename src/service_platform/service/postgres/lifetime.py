from asyncio import current_task

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from service_platform.settings import settings, logger


def init_postgres(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection for postgres.

    :param app: current fastapi application.
    """
    engine = create_async_engine(str(settings.postgres_url))
    session_factory = async_scoped_session(
        async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        ),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
    logger.info("postgres initialized")


def init_postgres_worker():
    engine = create_async_engine(
        url=str(settings.postgres_url),
        max_overflow=0,
        pool_timeout=30,
    )
    session_factory = async_scoped_session(
        async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        ),
        scopefunc=current_task,
    )
    return session_factory


async def shutdown_postgres(app: FastAPI) -> None:  # pragma: no cover
    """
    Closes postgres connectio.

    :param app: current FastAPI app.
    """
    await app.state.db_engine.dispose()
    logger.info("postgres disconnected")

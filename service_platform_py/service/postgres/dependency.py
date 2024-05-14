import asyncio
from typing import AsyncGenerator

from sqlalchemy import make_url, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.requests import Request

from service_platform_py.settings import settings


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session

    finally:
        await session.commit()
        await session.close()


async def create_database() -> None:
    """Create a database."""
    import logging

    logger = logging.getLogger(__name__)
    logger.debug(f'Creating database "{settings.db_name}"')
    db_url = make_url(str(settings.postgres_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{settings.db_name}'",  # noqa: E501, S608
            ),
        )
        database_exists = database_existance.scalar() == 1
    if database_exists:
        await drop_database()

    await asyncio.sleep(3)
    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f'CREATE DATABASE "{settings.db_name}" ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            ),
        )


async def drop_database() -> None:
    """Drop current database."""
    db_url = make_url(str(settings.postgres_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{settings.db_name}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{settings.db_name}"'))


def migrate() -> None:
    import subprocess

    subprocess.run(["ls", "-l"])
    subprocess.run(
        ["flyway", "-configFiles=flyway.test.conf", "clean", "migrate"],
        cwd="sql",
    )

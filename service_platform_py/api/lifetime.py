from service_platform_py.service.tkq.tkq import broker
from service_platform_py.settings import logger


async def register_startup_event() -> None:
    """
    Actions to run on application startup.
    This function uses fastAPI app to store data
    in the state, such as db_engine.
    :return: None.
    """
    if not broker.is_worker_process:
        await broker.startup()
        logger.info("broker started")


async def register_shutdown_event() -> None:
    """
    Actions to run on application's shutdown.
    :return: None.
    """
    if not broker.is_worker_process:
        await broker.shutdown()
        logger.info("broker shutdown")

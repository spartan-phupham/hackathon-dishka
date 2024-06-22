from service_platform.settings import logger
from service_platform.worker.example_worker import ExampleWorker


async def register_startup_event() -> None:
    """
    Actions to run on application startup.
    This function uses fastAPI app to store data
    in the state, such as db_engine.
    :return: None.
    """
    logger.info("registered startup event")


async def register_shutdown_event() -> None:
    """
    Actions to run on application's shutdown.
    :return: None.
    """
    logger.info("registered shutdown event")


async def register_worker() -> None:
    """
    Actions to run on application startup.
    This function uses fastAPI app to store data
    in the state, such as db_engine.
    :return: None.
    """
    example_worker = ExampleWorker()
    await example_worker.start()
    logger.info("registered worker")

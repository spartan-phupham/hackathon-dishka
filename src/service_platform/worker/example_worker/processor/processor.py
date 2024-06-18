import uuid

from service_platform.settings import logger
from service_platform.worker.example_worker.processor.schema import ExampleWorkerPayload
from service_platform.worker.example_worker.repository.respository import (
    ExampleWorkerRepository,
)


class ExampleWorkerProcessor:
    def __init__(
        self,
    ) -> None:
        self.repository = ExampleWorkerRepository()

    async def handle(self, message):
        payload = ExampleWorkerPayload()
        await self.process(payload)

    async def process(self, payload: ExampleWorkerPayload) -> None:
        logger.info(f"Handling payload {payload}")
        await self.repository.handler()

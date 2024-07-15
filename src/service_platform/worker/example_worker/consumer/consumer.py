import asyncio

from service_platform.service.aws.sqs import SQSConsumer
from service_platform.settings import settings
from service_platform.worker.example_worker.processor import ExampleWorkerProcessor


class ExampleWorkerConsumer:
    def __init__(
        self,
    ) -> None:
        processor = ExampleWorkerProcessor()
        self.sqs = SQSConsumer(
            queue_url=settings.aws.sqs.workers.example_worker.url,
            processors=[processor],
        )

    async def start(self) -> None:
        self.sqs.start()
        try:
            while True:
                await asyncio.sleep(1)
        finally:
            self.sqs.stop()

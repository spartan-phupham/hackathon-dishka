import asyncio

import nest_asyncio

from service_platform.settings import settings
from service_platform.worker.example_worker.consumer import ExampleWorkerConsumer

nest_asyncio.apply()


class ExampleWorker:
    def __init__(self):
        self.consumer = ExampleWorkerConsumer()

    async def start(self):
        consumers = [
            self.consumer
            for _ in range(settings.aws.sqs.workers.example_worker.number_of_consumers)
        ]
        await asyncio.gather(*[consumer.start() for consumer in consumers])

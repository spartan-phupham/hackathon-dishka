import asyncio
import json
from asyncio import CancelledError

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from service_platform.service.aws import aws_credentials_dummy
from service_platform.settings import logger, settings


class SQSConsumer:
    N_WORKERS = 8

    def __init__(self, queue_url, processors):
        self.client = boto3.client(
            "sqs",
            endpoint_url=settings.aws.endpoint_url,
            region_name=settings.aws.region,
            **aws_credentials_dummy,
        )
        self.queue_url = queue_url
        self.processors = processors
        self.supervisor_task = None
        self.message_queue = asyncio.Queue()

    def start(self):
        logger.info(f"SQS Start worker and poll from queue={self.queue_url}")
        self.supervisor_task = asyncio.ensure_future(self._supervisor())

    def stop(self):
        logger.info(f"SQS Stop worker and poll from queue={self.queue_url}")
        if self.supervisor_task:
            self.supervisor_task.cancel()

    async def _supervisor(self):
        consumer_task = asyncio.ensure_future(self._launch_consumer_loop())
        worker_tasks = [
            asyncio.ensure_future(self._launch_worker()) for _ in range(self.N_WORKERS)
        ]

        tasks = [consumer_task] + worker_tasks
        try:
            await asyncio.gather(*tasks)
        except CancelledError:
            logger.warning("SQS Job cancelled")
        except Exception as e:
            logger.warning(f"SQS Job failed, retrying... due to={e}")

    async def _launch_consumer_loop(self):
        while True:
            request = {
                "QueueUrl": self.queue_url,
                "WaitTimeSeconds": 20,
                "MaxNumberOfMessages": 10,
            }
            try:
                response = await asyncio.to_thread(
                    self.client.receive_message, **request
                )
                messages = response.get("Messages", [])
                for message in messages:
                    await self.message_queue.put(message)
            except (BotoCoreError, ClientError) as e:
                logger.warning(
                    f"SQS Failed to poll from queue={self.queue_url} due to={e}"
                )

    async def _launch_worker(self):
        while True:
            message = await self.message_queue.get()
            try:
                await self.process(message)
                await self.delete(message)
            except Exception as e:
                logger.warning(
                    f"SQS Failed to process message={message['Body']} due to={e}"
                )
                await self.change_visibility(message)

    async def process(self, message):
        try:
            for processor in self.processors:
                await processor.handle(json.loads(message["Body"]))
            return len(self.processors) > 0
        except Exception as e:
            logger.warning(
                f"SQS Failed to process message={message['Body']} due to={e}"
            )
            return False

    async def delete(self, message):
        request = {
            "QueueUrl": self.queue_url,
            "ReceiptHandle": message["ReceiptHandle"],
        }
        await asyncio.to_thread(self.client.delete_message, **request)
        logger.info(f"SQS Message deleted: {message['Body']}")

    async def change_visibility(self, message):
        request = {
            "QueueUrl": self.queue_url,
            "ReceiptHandle": message["ReceiptHandle"],
            "VisibilityTimeout": 10,
        }
        await asyncio.to_thread(self.client.change_message_visibility, **request)
        logger.info(f"SQS Changed visibility of message: {message['Body']}")

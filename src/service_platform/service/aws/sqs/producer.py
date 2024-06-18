import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from service_platform.service.aws import aws_credentials_dummy
from service_platform.settings import logger, settings


class SQSJobProducer:
    def __init__(self, queue_url):
        self.client = boto3.client(
            "sqs",
            endpoint_url=settings.aws.endpoint_url,
            region_name=settings.aws.region,
            **aws_credentials_dummy,
        )
        self.queue_url = queue_url

    async def send(self, payload: dict, delay_seconds: int | None = None) -> bool:
        try:
            if not self.queue_url:
                return False
            message = json.dumps(payload)
            params = {
                "QueueUrl": self.queue_url,
                "MessageBody": message,
            }
            if delay_seconds is not None and 1 <= delay_seconds <= 900:
                params["DelaySeconds"] = delay_seconds
            logger.info(f"SQS Message sent: {message}")
            self.client.send_message(**params)
            return True
        except (BotoCoreError, ClientError) as e:
            logger.warning(f"SQS Failed to send message={payload} due to={str(e)}")
            return False

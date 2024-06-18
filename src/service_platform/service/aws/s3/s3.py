import os
import uuid

import boto3
from fastapi import UploadFile

from service_platform.exception.server_error import ServerError
from service_platform.service.aws import aws_credentials_dummy
from service_platform.settings import logger, settings
from service_platform.utils.string_utils import StringUtils


class S3:
    def __init__(self, bucket) -> None:
        self.s3 = boto3.client(
            "s3", endpoint_url=settings.aws.endpoint_url, **aws_credentials_dummy
        )
        self.bucket = bucket
        self.region = settings.aws.region
        self.string_helper = StringUtils()

    async def upload(
        self, file: UploadFile, user_id: uuid.UUID, key: str | None = None
    ) -> str:
        try:
            if key is None:
                key = (
                    f"{user_id}/"
                    f"{self.string_helper.generate_random_string()}/{file.filename}"
                )
            self.s3.upload_fileobj(
                Fileobj=file.file,
                Bucket=self.bucket,
                Key=key,
                ExtraArgs={"ACL": "public-read"},
            )
            return key
        except Exception as e:
            logger.error(e)
            raise ServerError.INTERNAL_SERVER_ERROR.as_http_exception(
                custom_message="Failed to upload s3 file"
            )

    async def delete(self, key: str) -> None:
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
        except Exception as e:
            logger.error(e)
            raise ServerError.INTERNAL_SERVER_ERROR.as_http_exception(
                custom_message="Failed to delete s3 file"
            )

    async def move(self, old_key: str, new_key: str) -> None:
        try:
            self.s3.copy_object(
                Bucket=self.bucket,
                CopySource={"Bucket": self.bucket, "Key": old_key},
                Key=new_key,
            )
            self.s3.delete_object(Bucket=self.bucket, Key=old_key)
        except Exception as e:
            logger.error(e)
            raise ServerError.INTERNAL_SERVER_ERROR.as_http_exception(
                custom_message="Failed to delete s3 file"
            )

    async def download(self, key: str, file_name: str, folder: str) -> str:
        try:
            file_path = os.path.join(folder, file_name)
            if not os.path.exists(file_path):
                os.makedirs(folder, exist_ok=True)
                self.s3.download_file(Bucket=self.bucket, Key=key, Filename=file_path)
                logger.info(f"S3 Downloaded {key} to {file_name}")
            return file_path
        except Exception as e:
            logger.error(e)

    def generate_s3_url(self, key):
        if os.environ.get("ENVIRONMENT", "dev") == "local":
            return f"{settings.aws.endpoint_url}/{settings.aws.s3_bucket}/{key}"
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"

import logging
import os
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from yarl import URL

FILE_SETTING_PATH = Path(__file__)
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")


class LogLevel(str, Enum):
    """Possible log levels."""

    CRITICAL = "critical"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    TRACE = "trace"


class Environment(str, Enum):
    """Possible environment levels."""

    LOCAL = "local"
    DEV = "dev"
    PRODUCTION = "production"


def load_environment_keys(env_type: str) -> str:
    return (
        ".envs/fastapi/.env.local"
        if env_type == Environment.LOCAL
        else ".envs/fastapi/.env"
    )


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    address: str = "0.0.0.0"
    port: int = 8080
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = Environment.DEV.value

    # log level
    log_level: LogLevel = LogLevel.INFO

    # allow origin
    allowed_origin: str = ""

    # datadog
    enable_datadog: bool = False

    # db
    enable_db: bool = False
    db_url: str = "localhost"
    db_name: str = "db_py"
    db_username: str = "local"
    db_password: str = "local"
    db_port: int = 5432

    # redis
    enable_redis: bool = False
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[str] = None

    def __init__(self):
        env_file = load_environment_keys(ENVIRONMENT)
        super().__init__(_env_file=env_file, _env_file_encoding="utf-8")

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None and self.redis_base != "":
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    @property
    def postgres_url(self) -> URL:
        """
        Assemble POSTGRES URL from settings.

        :return: postgres URL.
        """
        return URL.build(
            # scheme="postgresql+psycopg2",
            scheme="postgresql+asyncpg",
            host=self.db_url,
            port=self.db_port,
            user=self.db_username,
            password=self.db_password,
            path=f"/{self.db_name}",
        )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = Settings()

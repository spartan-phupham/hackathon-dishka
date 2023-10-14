import enum
import logging
import os
from pathlib import Path
from tempfile import gettempdir
from typing import Any, Optional

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())
FILE_SETTING_PATH = Path(__file__)
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Environment(str, enum.Enum):  # noqa: WPS600
    """Possible environment levels."""

    DEV = "dev"
    TEST = "test"
    PRODUCT = "production"


class Settings(BaseSettings):  # noqa: WPS600
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = Environment.DEV.value

    log_level: LogLevel = LogLevel.INFO

    # Variables for Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None

    # Variables for OpenAI
    openai_api_key: str
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index_name: str = "spartan-openai"

    def __init__(self, **data: Any) -> None:
        """
        Initialize the settings object.

        :param **data: Load environment variable
        """
        self.load_environment_specific_keys(ENVIRONMENT)
        super().__init__(**data)

    def load_environment_specific_keys(self, env_type: str) -> None:
        """
        Load environment-specific keys based on the given environment.

        :param env_type: Type of environment run application
        """
        if env_type == Environment.TEST:
            env_file = (
                FILE_SETTING_PATH.resolve().parent.parent / ".envs/fastapi/.env.test"
            )
            self.__config__.env_file = env_file
            self.__config__.env_file_encoding = "utf-8"
        elif env_type == Environment.DEV:
            env_file = FILE_SETTING_PATH.resolve().parent.parent / ".envs/fastapi/.env"
            self.__config__.env_file = env_file
            self.__config__.env_file_encoding = "utf-8"

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings: Settings = Settings()

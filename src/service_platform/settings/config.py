from enum import Enum

from pydantic import BaseModel


class UvicornLogLevel(str, Enum):
    """Possible log levels."""

    CRITICAL = "critical"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    TRACE = "trace"


class LoggingLogLevel(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    NOTSET = "notset"


class LoggerSettings(BaseModel):
    level: LoggingLogLevel = LoggingLogLevel.INFO
    log_access: bool = False
    log_file: str = ""
    log_file_count: int = 5
    log_file_size: int = 1024 * 1024 * 10  # 10 MB


class Environment(str, Enum):
    """Possible environment levels."""

    LOCAL = "local"
    DEV = "dev"
    PRODUCTION = "production"


class ServerConfig(BaseModel):
    address: str = "0.0.0.0"
    port: int | None = 8080
    allowed_origin: str = ""
    reload: bool = False
    workers_count: int = 1
    proxy_headers: bool = True
    forwarded_allow_ips: str = "*"
    uvicorn_log_level: UvicornLogLevel = UvicornLogLevel.INFO
    max_upload_files: int = 10
    logger: LoggerSettings = LoggerSettings()


class DBConfig(BaseModel):
    enabled: bool = False
    address: str
    db_name: str
    username: str
    password: str
    port: int = 5432


class RedisConfig(BaseModel):
    enabled: bool = False
    address: str
    port: int = 6379
    username: str
    password: str
    base: int = 0


class DatadogSettings(BaseModel):
    enabled: bool = False


class JWTConfig(BaseModel):
    secret_key_base64: str
    public_key_base64: str
    algorithm: str = "RS512"
    expiration_time: int = 3600  # 1 hour
    refresh_expiration_time: int = 86400  # 1 day
    issuer: str = "service_platform"


class GoogleConfig(BaseModel):
    api_url: str = "https://www.googleapis.com"
    oauth_url: str = "https://oauth2.googleapis.com"
    client_id: str
    client_secret: str
    redirect_uri: str


class LinkedinConfig(BaseModel):
    api_url: str = "https://api.linkedin.com"
    oauth_url: str = "https://www.linkedin.com"
    client_id: str
    client_secret: str
    redirect_uri: str


class ZoomConfig(BaseModel):
    zoom_url: str = "https://zoom.us"
    api_url: str = "https://api.zoom.us"
    client_id: str
    client_secret: str
    redirect_uri: str


class Auth0Config(BaseModel):
    base_url: str
    client_id: str
    client_secret: str
    redirect_uri: str


class SQSWorkerDetailSetting(BaseModel):
    url: str
    number_of_consumers: int = 1


class SQSWorkerSettings(BaseModel):
    example_worker: SQSWorkerDetailSetting


class SQSSettings(BaseModel):
    localstack: bool = False
    workers: SQSWorkerSettings


class AWSConfig(BaseModel):
    endpoint_url: str | None = None
    region: str = "us-west-2"
    s3_bucket: str
    sqs: SQSSettings

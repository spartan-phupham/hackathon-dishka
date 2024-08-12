import logging.config
from typing import Any

from service_platform.settings import settings


class HealthCheckFilter(logging.Filter):
    def __init__(self, health_check_endpoint: str = "/health/"):
        super().__init__()
        self.health_check_endpoint = health_check_endpoint

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self.health_check_endpoint) == -1


def get_server_loggers():
    server_loggers = {
        "uvicorn": {
            "level": settings.server.logger.level.upper(),
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": settings.server.logger.level.upper(),
            "handlers": ["console"],
            "propagate": False,
        },
        "service_platform": {
            "level": settings.server.logger.level.upper(),
            "handlers": ["console"],
            "propagate": False,
        },
    }

    if settings.server.logger.log_access:
        server_loggers["uvicorn.access"] = {
            "level": settings.server.logger.level.upper(),
            "handlers": ["console"],
            "filters": ["heath_check"],
            "propagate": False,
        }
    else:
        logging.getLogger("uvicorn.access").disabled = True

    return server_loggers


def get_log_config():
    log_config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "heath_check": {
                "()": HealthCheckFilter,
                "health_check_endpoint": "/api/health/",
            },
        },
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "json": {
                "class": "service_platform.utils.logging.ddtrace_json_formatter.DdTraceJSONFormatter",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console"],
                "level": "WARN",
            },
        },
    }

    if settings._environment.lower() == "local":
        log_config["formatters"]["color"] = {
            "()": "colorlog.ColoredFormatter",
            "format": (
                "%(cyan)s%(asctime)s%(reset)s - "
                "%(blue)s%(name)s%(reset)s - "
                "%(log_color)s%(levelname)s%(reset)s - "
                "%(white)s%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            "secondary_log_colors": {},
            "style": "%",
        }
        # Use color formatter for console in local environment
        log_config["handlers"]["console"]["class"] = "colorlog.StreamHandler"
        log_config["handlers"]["console"]["formatter"] = "color"

    log_config["loggers"].update(get_server_loggers())

    if settings.server.logger.log_file:
        log_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": settings.server.logger.log_file,
            "maxBytes": settings.server.logger.log_file_size,
            "backupCount": settings.server.logger.log_file_count,
        }

        for server_logger in log_config["loggers"].values():
            server_logger["handlers"].append("file")

    return log_config


def config_logging():
    log_config = get_log_config()
    logging.config.dictConfig(log_config)

    return log_config

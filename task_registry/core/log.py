import copy
import logging
import logging.config
from typing import Any

from task_registry.core.types import LoggingLevelType

LOGGING_SIZE = 10 * 1024 * 1024
LOGGING_BACKUP_COUNT = 5

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "generic": {
            "()": "logging.Formatter",
            "style": "{",
            "fmt": "{asctime}({levelname},{name}): {message}",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
        }
    },
    "handlers": {
        "console": {
            "formatter": "generic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "httpcore": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

FILE_HANDLER_CONFIG = {
    "formatter": "generic",
    "()": "logging.handlers.RotatingFileHandler",
    "filename": "task-registry.log",
    "maxBytes": LOGGING_SIZE,
    "backupCount": LOGGING_BACKUP_COUNT,
}


def configure_logging(
    level: LoggingLevelType = "INFO", config: dict[str, Any] | None = None, log_to_file: bool = False
) -> None:
    log_config = copy.deepcopy(LOGGING_CONFIG)

    if log_to_file:
        log_config["handlers"]["file"] = FILE_HANDLER_CONFIG.copy()
        for logger_config in log_config["loggers"].values():
            logger_config["handlers"].append("file")

    if config:
        log_config.update(config)

    logging.config.dictConfig(log_config)

    logger = logging.getLogger("tr")

    logger.setLevel(level)

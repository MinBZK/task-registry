import logging
from typing import Any, TypeVar

from pydantic_settings import BaseSettings
from task_registry.core.types import EnvironmentType, LoggingLevelType

logger = logging.getLogger(__name__)


# Self type is not available in Python 3.10 so create our own with TypeVar
SelfSettings = TypeVar("SelfSettings", bound="Settings")

PROJECT_NAME: str = "Task Registry"
PROJECT_SUMMARY: str = """
API service for the task registry. This API can be used to retrieve
measures, requirements and instruments in this registry.
"""
VERSION: str = "0.1.0"  # replace in CI/CD pipeline
LICENSE_NAME: str = "EUPL-1.2 license"
LICENSE_URL: str = "https://eupl.eu/1.2/en/"


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentType = "local"

    LOGGING_LEVEL: LoggingLevelType = "INFO"
    LOGGING_CONFIG: dict[str, Any] | None = None
    LOG_TO_FILE: bool = False


def get_settings() -> Settings:
    return Settings()

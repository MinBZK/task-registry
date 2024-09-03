import logging
from typing import Any, TypeVar

from instrument_registry.core.types import EnvironmentType, LoggingLevelType
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


# Self type is not available in Python 3.10 so create our own with TypeVar
SelfSettings = TypeVar("SelfSettings", bound="Settings")

PROJECT_NAME: str = "IR"
PROJECT_DESCRIPTION: str = "Instrument Registry"
VERSION: str = "0.1.0"  # replace in CI/CD pipeline


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentType = "local"

    LOGGING_LEVEL: LoggingLevelType = "INFO"
    LOGGING_CONFIG: dict[str, Any] | None = None


def get_settings() -> Settings:
    return Settings()

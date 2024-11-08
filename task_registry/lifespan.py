import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from task_registry.core.config import PROJECT_NAME, VERSION, get_settings
from task_registry.core.log import configure_logging
from task_registry.data import CachedRegistry, TaskType

CACHED_REGISTRY = CachedRegistry()

configure_logging(get_settings().LOGGING_LEVEL, get_settings().LOGGING_CONFIG)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(f"Starting {PROJECT_NAME} version {VERSION}")

    CACHED_REGISTRY.add_tasks(TaskType.INSTRUMENTS)
    CACHED_REGISTRY.add_tasks(TaskType.MEASURES)
    CACHED_REGISTRY.add_tasks(TaskType.REQUIREMENTS)

    yield

    logger.info(f"Stopping application {PROJECT_NAME} version {VERSION}")
    logging.shutdown()

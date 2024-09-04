import json
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, TextIO

import yaml
from fastapi import FastAPI
from instrument_registry.core.config import PROJECT_NAME, VERSION, get_settings
from instrument_registry.core.log import configure_logging

cached_data: dict[str, Any] = {}

configure_logging(get_settings().LOGGING_LEVEL, get_settings().LOGGING_CONFIG)

logger = logging.getLogger(__name__)


def get_index_file() -> TextIO:
    return open("index.json")  # noqa: SIM115 # pragma: no cover


def get_instrument_file(path: str) -> TextIO:
    return open(path)  # noqa: SIM115 # pragma: no cover


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(f"Starting {PROJECT_NAME} version {VERSION}")
    with get_index_file() as f:
        cached_data["index"] = json.load(f)
    urn_mapper = {}
    for instrument in cached_data["index"]["entries"]:
        with get_instrument_file(instrument["path"]) as f:
            urn_mapper[instrument["urn"]] = yaml.safe_load(f)
    cached_data["urn_mapper"] = urn_mapper
    yield
    cached_data.clear()
    logger.info(f"Stopping application {PROJECT_NAME} version {VERSION}")
    logging.shutdown()

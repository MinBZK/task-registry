import io
import logging
from collections.abc import Generator
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from instrument_registry import lifespan
from instrument_registry.server import create_app

logger = logging.getLogger(__name__)

INDEX_JSON = """
{
    "entries": [
        {
            "path": "instruments/test_instrument.yaml",
            "urn": "test_urn"
        }
    ]
}
"""

INSTRUMENT_JSON = """{"test":"test"}"""


@pytest.fixture
def mock_index_file() -> Generator[None, None, None]:  # noqa: PT004
    origin = lifespan.get_index_file
    lifespan.get_index_file = Mock(return_value=io.StringIO(INDEX_JSON))
    yield
    lifespan.get_index_file = origin


@pytest.fixture
def mock_instrument_file() -> Generator[None, None, None]:  # noqa: PT004
    origin = lifespan.get_instrument_file
    lifespan.get_instrument_file = Mock(return_value=io.StringIO(INSTRUMENT_JSON))
    yield
    lifespan.get_instrument_file = origin


@pytest.fixture
def client(
    monkeypatch: pytest.MonkeyPatch,
    mock_index_file: Generator[None, None, None],
    mock_instrument_file: Generator[None, None, None],
) -> Generator[TestClient, None, None]:
    app = create_app()

    with TestClient(app, raise_server_exceptions=True) as c:
        c.timeout = 5
        yield c

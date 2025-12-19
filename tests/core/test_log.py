import logging
import tempfile
from pathlib import Path

import pytest
from task_registry.core.config import Settings
from task_registry.core.log import FILE_HANDLER_CONFIG, configure_logging


def test_logging_tr_module(caplog: pytest.LogCaptureFixture):
    config = {"loggers": {"tr": {"propagate": True}}}

    configure_logging(config=config)

    logger = logging.getLogger("tr")

    message = "This is a test log message"
    logger.debug(message)  # defaults to INFO level so debug is not printed
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)

    assert len(caplog.records) == 4
    assert caplog.records[0].message == message


def test_logging_submodule(caplog: pytest.LogCaptureFixture):
    config = {"loggers": {"tr": {"propagate": True}}}

    configure_logging(config=config)

    logger = logging.getLogger("tr.main")

    message = "This is a test log message"
    logger.debug(message)
    logger.info(message)  # should use module logger level
    logger.warning(message)
    logger.error(message)
    logger.critical(message)

    assert len(caplog.records) == 4
    assert caplog.records[0].message == message


def test_logging_config(caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(
        "LOGGING_CONFIG",
        '{"loggers": { "tr": {  "propagate": "True" }},"formatters": { "generic": {  "fmt": "{name}: {message}"}}}',
    )

    settings = Settings()

    configure_logging(config=settings.LOGGING_CONFIG)

    logger = logging.getLogger("tr")

    message = "This is a test log message with other formatting"
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)

    assert len(caplog.records) == 4


def test_logging_loglevel(caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    config = {"loggers": {"tr": {"propagate": True}}}

    configure_logging(config=config)

    monkeypatch.setenv("LOGGING_LEVEL", "ERROR")

    settings = Settings()

    configure_logging(config=config, level=settings.LOGGING_LEVEL)

    logger = logging.getLogger("tr.main")

    message = "This is a test log message with different logging level"
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)

    assert len(caplog.records) == 2


def test_logging_log_to_file(monkeypatch: pytest.MonkeyPatch) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test.log"
        monkeypatch.setitem(FILE_HANDLER_CONFIG, "filename", str(log_file))

        configure_logging(log_to_file=True)

        # Verify file handler was added to root logger
        root_logger = logging.getLogger()
        handler_classes = [type(h).__name__ for h in root_logger.handlers]
        assert "RotatingFileHandler" in handler_classes

        # Log a message and verify it's written to the file
        message = "This is a file log message"
        root_logger.info(message)

        # Flush handlers to ensure log is written
        for handler in root_logger.handlers:
            handler.flush()

        assert log_file.exists()
        log_content = log_file.read_text()
        assert message in log_content


def test_logging_log_to_file_disabled() -> None:
    # When log_to_file is False (default), no file handler should be added
    configure_logging(log_to_file=False)

    root_logger = logging.getLogger()
    handler_classes = [type(h).__name__ for h in root_logger.handlers]

    assert "RotatingFileHandler" not in handler_classes


def test_logging_log_to_file_setting(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOG_TO_FILE", "false")

    settings = Settings()

    assert settings.LOG_TO_FILE is False

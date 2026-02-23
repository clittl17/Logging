"""Unit tests for logger.py."""

import logging
import os
import tempfile

import pytest

from logger import get_logger


class TestGetLogger:
    def test_returns_logger_instance(self):
        log = get_logger("test.basic")
        assert isinstance(log, logging.Logger)

    def test_logger_name(self):
        log = get_logger("test.name")
        assert log.name == "test.name"

    def test_default_level_is_debug(self):
        log = get_logger("test.level")
        assert log.level == logging.DEBUG

    def test_custom_level(self):
        log = get_logger("test.custom_level", level=logging.WARNING)
        assert log.level == logging.WARNING

    def test_console_handler_added(self):
        log = get_logger("test.console")
        assert any(
            isinstance(h, logging.StreamHandler) for h in log.handlers
        )

    def test_no_duplicate_handlers_on_repeated_calls(self):
        name = "test.no_dup"
        get_logger(name)
        get_logger(name)
        log = logging.getLogger(name)
        assert len(log.handlers) == 1

    def test_file_handler_added_when_log_file_specified(self):
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as tmp:
            path = tmp.name
        try:
            log = get_logger("test.file", log_file=path)
            assert any(
                isinstance(h, logging.FileHandler) for h in log.handlers
            )
        finally:
            # Close all file handlers before removing the file on Windows.
            for h in log.handlers:
                h.close()
            os.unlink(path)

    def test_messages_written_to_file(self, tmp_path):
        log_path = str(tmp_path / "output.log")
        log = get_logger("test.write", log_file=log_path)
        log.info("hello from test")
        for h in log.handlers:
            h.flush()
        with open(log_path, encoding="utf-8") as f:
            content = f.read()
        assert "hello from test" in content

    def teardown_method(self, _method):
        """Remove all handlers from loggers created in tests to keep isolation."""
        for name in list(logging.Logger.manager.loggerDict.keys()):
            if name.startswith("test."):
                log = logging.getLogger(name)
                for h in list(log.handlers):
                    h.close()
                    log.removeHandler(h)

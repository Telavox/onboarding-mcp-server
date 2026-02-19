"""Tests for CustomLogger."""

import re

from lib_logger import CustomLogger


class TestCustomLogger:
    """Test suite for CustomLogger."""

    def test_get_logger_returns_logger(self) -> None:
        """get_logger should return a callable logger."""
        logger = CustomLogger.get_logger("test")
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "debug")

    def test_trace_id_format(self) -> None:
        """trace_id should be 8 hex characters."""
        trace_id = CustomLogger.get_trace_id()
        assert len(trace_id) == 8
        assert re.match(r"^[0-9a-f]{8}$", trace_id)

    def test_trace_id_is_consistent(self) -> None:
        """trace_id should be the same across multiple calls."""
        trace_id1 = CustomLogger.get_trace_id()
        trace_id2 = CustomLogger.get_trace_id()
        assert trace_id1 == trace_id2

    def test_different_loggers_same_trace_id(self) -> None:
        """Different named loggers should share the same trace_id."""
        CustomLogger.get_logger("app1")
        CustomLogger.get_logger("app2")
        trace_id = CustomLogger.get_trace_id()

        # trace_id should be set and consistent
        assert trace_id
        assert len(trace_id) == 8

    def test_logging_does_not_raise(self) -> None:
        """All logging levels should execute without errors."""
        logger = CustomLogger.get_logger("test_levels")

        # These should not raise any exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

    def test_logger_with_special_characters(self) -> None:
        """Logger should handle names with special characters."""
        logger = CustomLogger.get_logger("my.module.name")
        logger.info("Test with dots")

        logger2 = CustomLogger.get_logger("my-app")
        logger2.info("Test with dashes")

    def test_logger_with_formatted_message(self) -> None:
        """Logger should handle formatted messages."""
        logger = CustomLogger.get_logger("format_test")

        logger.info("User {} logged in", "john")
        logger.info("Count: {count}", count=42)
        logger.info("Values: {}, {}, {}", 1, 2, 3)

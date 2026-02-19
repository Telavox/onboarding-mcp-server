"""Integration tests for logging system."""

import logging

from lib_logger import (
    InterceptHandler,
    LoggerCore,
    configure_fastapi_logging,
    configure_logging,
    reset_logging,
)
from lib_logger.adapters import ConsoleAdapter


class TestLoggingConfiguration:
    """Test suite for logging configuration."""

    def setup_method(self) -> None:
        """Reset logging before each test."""
        reset_logging()

    def test_configure_logging_basic(self) -> None:
        """configure_logging should set up logging successfully."""
        configure_logging()

        assert LoggerCore.is_configured()
        logger = LoggerCore.get_logger("test")
        assert logger is not None

    def test_configure_logging_with_adapters(self) -> None:
        """configure_logging should accept custom adapters."""
        from lib_logger.adapters import JSONAdapter

        configure_logging(
            adapters=[
                ConsoleAdapter(level="INFO"),
                JSONAdapter(level="DEBUG"),
            ]
        )

        assert LoggerCore.is_configured()
        assert len(LoggerCore.get_adapters()) == 2

    def test_configure_logging_idempotent(self) -> None:
        """configure_logging should be idempotent."""
        configure_logging()
        configure_logging()  # Should not raise or reconfigure

        assert LoggerCore.is_configured()

    def test_configure_fastapi_logging(self) -> None:
        """configure_fastapi_logging should set up FastAPI logging."""
        configure_fastapi_logging()

        assert LoggerCore.is_configured()
        logger = LoggerCore.get_logger("test")
        assert logger is not None

    def test_configure_with_stdlib_interception(self) -> None:
        """Should intercept stdlib logging when enabled."""
        configure_logging(intercept_stdlib=True)

        # Verify uvicorn logger has InterceptHandler
        uvicorn_logger = logging.getLogger("uvicorn")
        assert len(uvicorn_logger.handlers) > 0
        assert isinstance(uvicorn_logger.handlers[0], InterceptHandler)

    def test_configure_without_stdlib_interception(self) -> None:
        """Should not intercept stdlib logging when disabled."""
        # Clear any existing handlers first
        logging.getLogger("uvicorn").handlers = []

        configure_logging(intercept_stdlib=False)

        # uvicorn logger should not have InterceptHandler
        uvicorn_logger = logging.getLogger("uvicorn")
        if uvicorn_logger.handlers:
            assert not any(
                isinstance(h, InterceptHandler) for h in uvicorn_logger.handlers
            )

    def test_custom_stdlib_loggers(self) -> None:
        """Should intercept only specified stdlib loggers."""
        configure_logging(intercept_stdlib=True, stdlib_loggers=["custom_logger"])

        custom_logger = logging.getLogger("custom_logger")
        assert len(custom_logger.handlers) > 0
        assert isinstance(custom_logger.handlers[0], InterceptHandler)


class TestInterceptHandler:
    """Test suite for InterceptHandler."""

    def setup_method(self) -> None:
        """Reset logging before each test."""
        reset_logging()
        configure_logging()  # Setup lib_logger

    def test_intercepthandler_emit(self) -> None:
        """InterceptHandler should emit log records."""
        handler = InterceptHandler()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # Should not raise
        handler.emit(record)

    def test_stdlib_logging_through_interceptor(self) -> None:
        """Standard library logging should work through InterceptHandler."""
        # Setup interception
        stdlib_logger = logging.getLogger("test_stdlib")
        stdlib_logger.handlers = [InterceptHandler()]
        stdlib_logger.propagate = False

        # Should not raise
        stdlib_logger.info("Test message")
        stdlib_logger.warning("Warning message")
        stdlib_logger.error("Error message")

    def test_intercepthandler_with_exception(self) -> None:
        """InterceptHandler should handle exceptions in log records."""
        handler = InterceptHandler()

        try:
            raise ValueError("Test error")
        except ValueError:
            record = logging.LogRecord(
                name="test",
                level=logging.ERROR,
                pathname="test.py",
                lineno=1,
                msg="Error occurred",
                args=(),
                exc_info=None,
            )

            # Should not raise
            handler.emit(record)


class TestLoggerCore:
    """Test suite for LoggerCore."""

    def setup_method(self) -> None:
        """Reset logging before each test."""
        reset_logging()

    def test_get_logger_returns_logger(self) -> None:
        """get_logger should return a logger instance."""
        logger = LoggerCore.get_logger("test")

        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_get_logger_auto_configures(self) -> None:
        """get_logger should auto-configure if not configured."""
        assert not LoggerCore.is_configured()

        logger = LoggerCore.get_logger("test")

        assert LoggerCore.is_configured()
        assert logger is not None

    def test_logging_does_not_raise(self) -> None:
        """All logging operations should execute without errors."""
        logger = LoggerCore.get_logger("test")

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

    def test_logger_with_extra_data(self) -> None:
        """Logger should accept extra data."""
        logger = LoggerCore.get_logger("test")

        # Should not raise
        logger.info("User action", user_id="user_123", action="login")
        logger.error("Database error", table="users", error_code=500)

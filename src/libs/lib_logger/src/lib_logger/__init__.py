"""Advanced logging library with adapter support and async-safe trace IDs.

This library provides:
- Multiple output adapters (Console, JSON, GCP Cloud Logging)
- Async-safe trace ID management using contextvars
- Standard library logging interception (FastAPI, uvicorn, etc.)
- Backward-compatible CustomLogger API

Quick Start:
    Basic usage (backward compatible):
        from lib_logger import CustomLogger

        logger = CustomLogger.get_logger("my_app")
        logger.info("Application started")
        trace_id = CustomLogger.get_trace_id()

    Advanced usage with adapters:
        from lib_logger import configure_logging
        from lib_logger.adapters import ConsoleAdapter, JSONAdapter

        configure_logging(adapters=[
            ConsoleAdapter(level="INFO"),
            JSONAdapter(level="DEBUG")
        ])

    FastAPI integration:
        from lib_logger import configure_fastapi_logging
        from lib_logger.adapters import ConsoleAdapter

        app = FastAPI()
        configure_fastapi_logging(adapters=[ConsoleAdapter()])
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from lib_logger.config import (
    configure_fastapi_logging,
    configure_logging,
    configure_logging_from_env,
    reset_logging,
)
from lib_logger.core import LoggerCore
from lib_logger.interceptor import InterceptHandler

if TYPE_CHECKING:
    from loguru import Logger


class CustomLogger:
    """Backward-compatible logger wrapper (legacy API).

    This class maintains the original CustomLogger API for backward compatibility.
    New code should use configure_logging() and LoggerCore directly.

    Usage:
        from lib_logger import CustomLogger

        logger = CustomLogger.get_logger("my_app")
        logger.info("Application started")

        # Get trace ID for current context
        trace_id = CustomLogger.get_trace_id()

    Note:
        This wrapper uses LoggerCore internally. For new projects, consider
        using configure_logging() for more flexibility.
    """

    @classmethod
    def get_logger(cls, name: str) -> Logger:
        """Get a named logger instance.

        Args:
            name: Logger name, typically the module or app name.

        Returns:
            A loguru logger bound to the given name and trace_id.
        """
        return LoggerCore.get_logger(name)

    @classmethod
    def get_trace_id(cls) -> str:
        """Get the trace ID for the current async context.

        Returns:
            The 8-character trace ID.
        """
        return LoggerCore.get_trace_id()

    @classmethod
    def set_trace_id(cls, trace_id: str) -> None:
        """Set a custom trace ID for the current context.

        Args:
            trace_id: Custom trace ID to use.
        """
        LoggerCore.set_trace_id(trace_id)

    @classmethod
    def reset_trace_id(cls) -> None:
        """Reset trace ID for current context."""
        LoggerCore.reset_trace_id()


__all__ = [
    # Core
    "CustomLogger",  # Backward compatible
    "LoggerCore",  # New API
    # Configuration
    "configure_logging",
    "configure_logging_from_env",
    "configure_fastapi_logging",
    "reset_logging",
    # Interception
    "InterceptHandler",
]

"""Core logger implementation with contextvars for async-safe trace IDs."""

from __future__ import annotations

import uuid
from contextvars import ContextVar
from typing import TYPE_CHECKING

from loguru import logger as _loguru_logger

if TYPE_CHECKING:
    from loguru import Logger

    from lib_logger.adapters.base import BaseAdapter

# Context variable for async-safe trace ID storage
_trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")


class LoggerCore:
    """Core logger management with adapter support and async-safe trace IDs.

    Uses contextvars to maintain separate trace IDs for each async context,
    ensuring proper request correlation in async applications like FastAPI.

    Features:
    - Async-safe trace IDs using contextvars
    - Multiple output adapters (Console, JSON, GCP, etc.)
    - Standard library logging integration
    - Named loggers for different modules
    - Automatic trace ID generation per request/context
    """

    _configured: bool = False
    _adapters: list[BaseAdapter] = []

    @classmethod
    def configure(cls, adapters: list[BaseAdapter] | None = None) -> None:
        """Configure logging with specified adapters.

        Args:
            adapters: List of adapter instances. If None, uses ConsoleAdapter.
        """
        if cls._configured:
            return

        # Import here to avoid circular imports
        from lib_logger.adapters import ConsoleAdapter

        if adapters is None:
            adapters = [ConsoleAdapter()]

        cls._adapters = adapters

        # Remove default loguru handler
        _loguru_logger.remove()

        # Add all adapter sinks
        for adapter in cls._adapters:
            sink_config = adapter.get_sink_config()
            _loguru_logger.add(**sink_config)

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> Logger:
        """Get a named logger instance.

        Args:
            name: Logger name, typically the module or class name.

        Returns:
            A loguru logger bound to the given name and current trace_id.
        """
        cls.configure()
        trace_id = cls.get_trace_id()
        return _loguru_logger.bind(name=name, trace_id=trace_id)

    @classmethod
    def get_trace_id(cls) -> str:
        """Get the trace ID for the current async context.

        Returns a unique trace ID for the current context. In async applications,
        each request/task gets its own trace ID automatically.

        Returns:
            The 8-character trace ID for current context.
        """
        trace_id = _trace_id_var.get()
        if not trace_id:
            trace_id = uuid.uuid4().hex[:8]
            _trace_id_var.set(trace_id)
        return trace_id

    @classmethod
    def set_trace_id(cls, trace_id: str) -> None:
        """Set a custom trace ID for the current context.

        Useful for propagating trace IDs from external systems
        (e.g., X-Trace-Id headers, OpenTelemetry).

        Args:
            trace_id: Custom trace ID to use.
        """
        _trace_id_var.set(trace_id)

    @classmethod
    def reset_trace_id(cls) -> None:
        """Reset trace ID for current context.

        Generates a new trace ID for the current async context.
        Useful at the start of new requests or tasks.
        """
        trace_id = uuid.uuid4().hex[:8]
        _trace_id_var.set(trace_id)

    @classmethod
    def is_configured(cls) -> bool:
        """Check if logger is configured.

        Returns:
            True if configure() has been called.
        """
        return cls._configured

    @classmethod
    def get_adapters(cls) -> list[BaseAdapter]:
        """Get list of configured adapters.

        Returns:
            List of active adapter instances.
        """
        return cls._adapters.copy()

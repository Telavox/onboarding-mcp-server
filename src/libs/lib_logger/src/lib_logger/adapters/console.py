"""Console adapter for colorized terminal output."""

import sys
from typing import Any

from lib_logger.adapters.base import BaseAdapter


class ConsoleAdapter(BaseAdapter):
    """Console adapter with colored output (default adapter).

    Outputs logs to stderr with ANSI color codes for better readability.
    Format: timestamp | level | trace_id | name | file:line | message

    Example:
        2026-02-05 21:55:32 | INFO     | 05556afc | api | main.py:42 | Request received
    """

    def __init__(self, level: str = "DEBUG", colorize: bool = True, **kwargs: Any):
        """Initialize console adapter.

        Args:
            level: Minimum log level
            colorize: Enable ANSI color codes
            **kwargs: Additional configuration
        """
        super().__init__(level, **kwargs)
        self.colorize = colorize

    def format_record(self, record: dict[str, Any]) -> str:
        """Format record for console output (not used with loguru format string)."""
        return ""  # Loguru handles formatting via format string

    def get_sink_config(self) -> dict[str, Any]:
        """Get console sink configuration.

        Returns:
            Loguru sink config for colorized console output
        """
        return {
            "sink": sys.stderr,
            "format": (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<dim>{extra[trace_id]}</dim> | "
                "<cyan>{extra[name]}</cyan> | "
                "<dim>{file}:{line}</dim> | "
                "<level>{message}</level>"
            ),
            "level": self.level,
            "colorize": self.colorize,
        }

"""JSON adapter for structured logging output."""

import sys
from typing import Any

from lib_logger.adapters.base import BaseAdapter


class JSONAdapter(BaseAdapter):
    """JSON adapter for structured logging.

    Outputs logs as JSON objects, one per line. Ideal for log aggregation
    systems like Elasticsearch, Splunk, or cloud logging services.

    Example:
        {"timestamp": "2026-02-05T21:55:32.123Z", "level": "INFO",
         "trace_id": "05556afc", "name": "api", "message": "Request received",
         "file": "main.py", "line": 42}
    """

    def __init__(self, level: str = "DEBUG", **kwargs: Any):
        """Initialize JSON adapter.

        Args:
            level: Minimum log level
            **kwargs: Additional configuration
        """
        super().__init__(level, **kwargs)

    def format_record(self, record: dict[str, Any]) -> str:
        """Format record as JSON (handled by loguru serialize)."""
        return ""  # Loguru handles JSON serialization

    def get_sink_config(self) -> dict[str, Any]:
        """Get JSON sink configuration.

        Returns:
            Loguru sink config for JSON output
        """
        return {
            "sink": sys.stdout,
            "format": "{message}",
            "level": self.level,
            "serialize": True,  # Enable JSON serialization
            "colorize": False,
        }

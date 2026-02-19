"""Google Cloud Platform adapter for Cloud Logging.

This adapter emits one JSON object per line to stdout, following Google Cloud
structured logging conventions (Cloud Run, GKE, Compute Engine).
"""

import re
import sys
from datetime import timezone
from typing import Any

from lib_logger.adapters.base import BaseAdapter


class GCPAdapter(BaseAdapter):
    """Google Cloud Platform logging adapter.

    Formats logs for Google Cloud Logging with proper severity levels
    and structured fields. Compatible with Cloud Run, GKE, and Compute Engine.

    GCP Logging expects JSON with specific fields:
    - severity: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - message: Log message
    - timestamp: ISO 8601 timestamp
    - trace: Trace identifier for request correlation
    - sourceLocation: File, line, function

    Example:
        {"severity": "INFO", "message": "Request received",
         "trace": "projects/my-project/traces/05556afc",
         "timestamp": "2026-02-05T21:55:32.123Z",
         "sourceLocation": {"file": "main.py", "line": "42", "function": "handle_request"}}
    """

    def __init__(
        self, level: str = "DEBUG", project_id: str | None = None, **kwargs: Any
    ):
        """Initialize GCP adapter.

        Args:
            level: Minimum log level
            project_id: GCP project ID (optional, for full trace format)
            **kwargs: Additional configuration
        """
        super().__init__(level, **kwargs)
        self.project_id = project_id

    def format_record(self, record: dict[str, Any]) -> str:
        """Format record for GCP (handled by custom formatter)."""
        return ""  # Custom formatter handles GCP format

    @staticmethod
    def _is_gcp_trace_id(value: str) -> bool:
        """Return True if value looks like a GCP trace id (32 hex chars)."""
        return bool(re.fullmatch(r"[0-9a-f]{32}", value))

    @staticmethod
    def _json_default(value: Any) -> str:
        """Fallback serializer for non-JSON-serializable values."""
        return str(value)

    def _gcp_formatter(self, record: dict[str, Any]) -> str:
        """Format log record for Google Cloud Logging.

        Args:
            record: Loguru record dict

        Returns:
            JSON formatted for GCP
        """
        import json

        # Map loguru levels to GCP severity
        level_map = {
            "TRACE": "DEBUG",
            "DEBUG": "DEBUG",
            "INFO": "INFO",
            "SUCCESS": "INFO",
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL",
        }

        severity = level_map.get(record["level"].name, "INFO")

        # Build GCP-compatible log entry
        record_time = record["time"]
        record_dt = (
            record_time.datetime if hasattr(record_time, "datetime") else record_time
        ).astimezone(timezone.utc)
        log_entry = {
            "severity": severity,
            "message": record["message"],
            "timestamp": record_dt.isoformat().replace("+00:00", "Z"),
            "logging.googleapis.com/sourceLocation": {
                "file": record["file"].name,
                "line": record["line"],
                "function": record["function"],
            },
        }

        # Add trace information.
        # NOTE: Google Cloud expects a 32-hex trace id for logging.googleapis.com/trace.
        trace_id = str(record["extra"].get("trace_id", "") or "")
        if trace_id:
            # Always include a trace_id field for internal correlation.
            log_entry["trace_id"] = trace_id

            # Only set the official GCP trace field if it is valid.
            if self.project_id and self._is_gcp_trace_id(trace_id):
                log_entry["logging.googleapis.com/trace"] = (
                    f"projects/{self.project_id}/traces/{trace_id}"
                )

        # Add logger name
        logger_name = record["extra"].get("name")
        if logger_name:
            log_entry["logger"] = str(logger_name)

        # Add any extra fields
        for key, value in record["extra"].items():
            if key not in ["trace_id", "name"]:
                log_entry[key] = value

        return json.dumps(log_entry, default=self._json_default, ensure_ascii=False)

    def _sink(self, message: Any) -> None:
        """Write a single structured log line to stdout.

        Loguru passes a `Message` object to callable sinks. The message contains
        the original `record` dict, which we transform into a GCP-compatible
        JSON payload.
        """
        record = message.record
        sys.stdout.write(self._gcp_formatter(record) + "\n")

    def get_sink_config(self) -> dict[str, Any]:
        """Get GCP sink configuration.

        Returns:
            Loguru sink config for GCP Cloud Logging format
        """
        return {
            "sink": self._sink,
            "level": self.level,
            "colorize": False,
        }

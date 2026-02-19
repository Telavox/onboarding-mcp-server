"""Base adapter interface for logging outputs."""

from abc import ABC, abstractmethod
from typing import Any


class BaseAdapter(ABC):
    """Abstract base class for logging adapters.

    Adapters control how log messages are formatted and where they are sent.
    Each adapter receives structured log data and outputs it in a specific format.
    """

    def __init__(self, level: str = "DEBUG", **kwargs: Any):
        """Initialize adapter.

        Args:
            level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            **kwargs: Additional adapter-specific configuration
        """
        self.level = level
        self.config = kwargs

    @abstractmethod
    def format_record(self, record: dict[str, Any]) -> str:
        """Format a log record for output.

        Args:
            record: Log record with keys like 'time', 'level', 'message', 'name',
                   'trace_id', 'file', 'line', 'function', 'extra'

        Returns:
            Formatted log message string
        """
        pass

    @abstractmethod
    def get_sink_config(self) -> dict[str, Any]:
        """Get loguru sink configuration.

        Returns:
            Dictionary with loguru add() parameters:
            - sink: Output destination
            - format: Format function or string
            - level: Minimum level
            - colorize: Enable colors
            - serialize: Enable JSON output
            - etc.
        """
        pass

    def should_log(self, level: str) -> bool:
        """Check if a log level should be logged.

        Args:
            level: Log level to check

        Returns:
            True if level should be logged
        """
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        min_level_idx = levels.index(self.level.upper())
        current_level_idx = levels.index(level.upper())
        return current_level_idx >= min_level_idx

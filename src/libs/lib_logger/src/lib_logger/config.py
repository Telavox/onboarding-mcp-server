"""Configuration helpers for logging setup."""

import logging
import os
from typing import Any

from lib_logger.adapters import ConsoleAdapter, GCPAdapter
from lib_logger.adapters.base import BaseAdapter
from lib_logger.core import LoggerCore
from lib_logger.interceptor import InterceptHandler

LOG_ENV_VAR = "LOG_ENV"
GOOGLE_ENV_VALUE = "google"
LOG_LEVEL_VAR = "LOG_LEVEL"
PROJECT_ID_VARS = ("GOOGLE_CLOUD_PROJECT", "GCP_PROJECT_ID")


def configure_logging(
    adapters: list[BaseAdapter] | None = None,
    intercept_stdlib: bool = True,
    stdlib_loggers: list[str] | None = None,
) -> None:
    """Configure comprehensive logging for applications.

    Sets up loguru with specified adapters and optionally intercepts
    standard library logging (e.g., from FastAPI, uvicorn, sqlalchemy).

    Args:
        adapters: List of adapter instances. If None, uses ConsoleAdapter.
        intercept_stdlib: Whether to intercept stdlib logging
        stdlib_loggers: Specific loggers to intercept. If None, intercepts:
                       ["uvicorn", "uvicorn.access", "uvicorn.error",
                        "fastapi", "sqlalchemy", "sqlalchemy.engine"]

    Example:
        from lib_logger import configure_logging
        from lib_logger.adapters import ConsoleAdapter, JSONAdapter

        # Console + JSON output
        configure_logging(adapters=[ConsoleAdapter(), JSONAdapter()])

        # For FastAPI
        from fastapi import FastAPI
        app = FastAPI()
        configure_logging()  # Intercepts uvicorn/fastapi logs automatically
    """
    # Configure loguru with adapters
    LoggerCore.configure(adapters=adapters)

    if not intercept_stdlib:
        return

    # Default stdlib loggers to intercept
    if stdlib_loggers is None:
        stdlib_loggers = [
            "uvicorn",
            "uvicorn.access",
            "uvicorn.error",
            "fastapi",
            "sqlalchemy",
            "sqlalchemy.engine",
        ]

    # Setup interception
    for logger_name in stdlib_loggers:
        stdlib_logger = logging.getLogger(logger_name)
        stdlib_logger.handlers = [InterceptHandler()]
        stdlib_logger.propagate = False


def configure_fastapi_logging(
    adapters: list[BaseAdapter] | None = None, **kwargs: Any
) -> None:
    """Configure logging specifically for FastAPI applications.

    Convenience function that sets up logging with sensible defaults
    for FastAPI apps, including uvicorn access logs.

    Args:
        adapters: List of adapter instances
        **kwargs: Additional arguments passed to configure_logging()

    Example:
        from fastapi import FastAPI
        from lib_logger import configure_fastapi_logging
        from lib_logger.adapters import ConsoleAdapter

        app = FastAPI()
        configure_fastapi_logging(adapters=[ConsoleAdapter(level="INFO")])
    """
    configure_logging(
        adapters=adapters,
        intercept_stdlib=True,
        stdlib_loggers=[
            "uvicorn",
            "uvicorn.access",
            "uvicorn.error",
            "fastapi",
        ],
        **kwargs,
    )


def configure_logging_from_env(**kwargs: Any) -> None:
    """Configure logging based on environment variables.

    Selects GCP adapter when LOG_ENV matches the provided value, otherwise
    falls back to console output.

    Args:
        **kwargs: Additional arguments passed to configure_logging().
    """
    log_env = os.environ.get(LOG_ENV_VAR, "").strip().lower()
    level = os.environ.get(LOG_LEVEL_VAR, "INFO")

    project_id = None
    for var in PROJECT_ID_VARS:
        project_id = os.environ.get(var)
        if project_id:
            break

    adapters: list[BaseAdapter]
    if log_env == GOOGLE_ENV_VALUE:
        adapters = [GCPAdapter(level=level, project_id=project_id)]
    else:
        adapters = [ConsoleAdapter(level=level)]

    configure_logging(adapters=adapters, **kwargs)


def reset_logging() -> None:
    """Reset logging configuration.

    Useful for testing or when you need to reconfigure logging.
    """
    from loguru import logger as _loguru_logger

    _loguru_logger.remove()
    LoggerCore._configured = False
    LoggerCore._adapters = []

    # Reset stdlib logging
    logging.basicConfig(force=True)

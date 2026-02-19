"""InterceptHandler to redirect standard library logging to loguru."""

import logging

from loguru import logger as _loguru_logger

from lib_logger.core import LoggerCore


class InterceptHandler(logging.Handler):
    """Intercepts standard library logging and redirects to loguru.

    This handler captures logs from libraries that use Python's standard
    logging module (like FastAPI, uvicorn, sqlalchemy) and routes them
    through loguru for consistent formatting.

    Usage:
        import logging
        from lib_logger import InterceptHandler

        # Replace all logging handlers with InterceptHandler
        logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)

        # Or for specific loggers
        logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    """

    def emit(self, record: logging.LogRecord) -> None:
        """Process a log record from stdlib logging.

        Args:
            record: Standard library LogRecord
        """
        # Get corresponding loguru level
        try:
            level = _loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the logging call was made
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Get current trace_id from context
        trace_id = LoggerCore.get_trace_id()

        # Log to loguru with proper context including trace_id and name
        _loguru_logger.opt(depth=depth, exception=record.exc_info).bind(
            trace_id=trace_id,
            name=record.name,  # Add logger name from stdlib logging
        ).log(level, record.getMessage())

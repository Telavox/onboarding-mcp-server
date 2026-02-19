"""Example demonstrating different adapters (Console, JSON, GCP)."""

from lib_logger import LoggerCore, configure_logging
from lib_logger.adapters import ConsoleAdapter, GCPAdapter, JSONAdapter


def example_console_only() -> None:
    """Example 1: Console output only (default behavior)."""
    print("\n=== Example 1: Console Adapter Only ===\n")

    configure_logging(adapters=[ConsoleAdapter(level="DEBUG")])

    logger = LoggerCore.get_logger("app")
    logger.debug("Debug message with colors")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")


def example_json_only() -> None:
    """Example 2: JSON output for structured logging."""
    print("\n=== Example 2: JSON Adapter Only ===\n")

    # Reset to reconfigure
    from lib_logger import reset_logging

    reset_logging()

    configure_logging(adapters=[JSONAdapter(level="INFO")])

    logger = LoggerCore.get_logger("api")
    logger.info("User logged in", user_id="user_123", ip="192.168.1.1")
    logger.warning("Rate limit approaching", requests=95, limit=100)
    logger.error("Database connection failed", error="Connection timeout")


def example_multiple_outputs() -> None:
    """Example 3: Multiple adapters - Console + JSON simultaneously."""
    print("\n=== Example 3: Console + JSON (Multiple Outputs) ===\n")

    from lib_logger import reset_logging

    reset_logging()

    # Configure both adapters
    configure_logging(
        adapters=[
            ConsoleAdapter(level="DEBUG"),  # Colored console output
            JSONAdapter(level="INFO"),  # Structured JSON output
        ]
    )

    logger = LoggerCore.get_logger("service")
    logger.debug("This appears in console only (DEBUG)")
    logger.info("This appears in both console AND JSON (INFO)")
    logger.error("Error in both outputs", error_code=500)


def example_gcp_format() -> None:
    """Example 4: Google Cloud Logging format."""
    print("\n=== Example 4: GCP Cloud Logging Format ===\n")

    from lib_logger import reset_logging

    reset_logging()

    configure_logging(adapters=[GCPAdapter(level="INFO")])

    logger = LoggerCore.get_logger("gcp-service")
    logger.info("Application started", version="1.2.3", environment="production")
    logger.warning("High memory usage detected", memory_mb=890, threshold_mb=800)
    logger.error("Service unavailable", service="database", region="us-central1")


def example_filtered_levels() -> None:
    """Example 5: Different log levels per adapter."""
    print("\n=== Example 5: Filtered Levels Per Adapter ===\n")

    from lib_logger import reset_logging

    reset_logging()

    configure_logging(
        adapters=[
            ConsoleAdapter(level="INFO"),  # Only INFO+ to console
            JSONAdapter(level="DEBUG"),  # All logs to JSON
        ]
    )

    logger = LoggerCore.get_logger("filtered")
    logger.debug("Debug log - only in JSON")
    logger.info("Info log - in both outputs")
    logger.error("Error log - in both outputs")


if __name__ == "__main__":
    print("=" * 60)
    print("lib_logger Adapter Examples")
    print("=" * 60)

    example_console_only()
    example_json_only()
    example_multiple_outputs()
    example_gcp_format()
    example_filtered_levels()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)

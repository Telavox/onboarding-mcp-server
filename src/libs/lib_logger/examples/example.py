"""Simple example using CustomLogger (backward compatible API).

For more advanced examples, see:
- example_adapters.py - Multiple output adapters (Console, JSON, GCP)
- example_fastapi.py  - FastAPI integration with unified logging
- example_async.py    - Async contexts and trace ID isolation
"""

from lib_logger import CustomLogger

# Create loggers for different modules
api_logger = CustomLogger.get_logger("api")
db_logger = CustomLogger.get_logger("database")
auth_logger = CustomLogger.get_logger("auth")


def handle_request() -> None:
    """Simulate handling an API request."""
    api_logger.info("Received GET /users")

    # Auth check
    auth_logger.debug("Validating token")
    auth_logger.info("User authenticated: user_123")

    # Database query
    db_logger.info("Querying users table")
    db_logger.debug("SELECT * FROM users WHERE active = true")

    # Response
    api_logger.info("Returning 200 OK with 42 users")


def handle_error() -> None:
    """Simulate an error scenario."""
    api_logger.info("Received POST /orders")
    db_logger.warning("Connection pool running low: 2/10 available")

    try:
        raise ValueError("Invalid order data")
    except ValueError:
        api_logger.error("Failed to process order: Invalid order data")


if __name__ == "__main__":
    print("=" * 60)
    print("lib_logger Basic Example (CustomLogger API)")
    print("=" * 60)
    print(f"Trace ID for this execution: {CustomLogger.get_trace_id()}")
    print("=" * 60)
    print()

    handle_request()
    print()
    handle_error()

    print()
    print("=" * 60)
    print("Example complete!")
    print()
    print("For more examples:")
    print("  - python examples/example_adapters.py")
    print("  - python examples/example_fastapi.py")
    print("  - python examples/example_async.py")
    print("=" * 60)

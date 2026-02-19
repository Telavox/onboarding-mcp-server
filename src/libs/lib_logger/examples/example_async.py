"""Example demonstrating async trace ID isolation with contextvars.

Shows how each async task gets its own isolated trace ID automatically.
"""

import asyncio

from lib_logger import LoggerCore, configure_logging
from lib_logger.adapters import ConsoleAdapter

# Configure logging once at startup
configure_logging(adapters=[ConsoleAdapter(level="DEBUG")])


async def process_order(order_id: int, delay: float) -> None:
    """Simulate processing an order with its own trace ID.

    Each concurrent task will have a unique trace ID, even though
    they're running simultaneously.
    """
    # Reset trace ID for this task context
    LoggerCore.reset_trace_id()
    trace_id = LoggerCore.get_trace_id()

    logger = LoggerCore.get_logger("order_processor")

    logger.info("Started processing order", order_id=order_id, trace_id=trace_id)

    # Simulate some async work
    await asyncio.sleep(delay)
    logger.debug("Validating order", order_id=order_id)

    await asyncio.sleep(delay)
    logger.debug("Processing payment", order_id=order_id)

    await asyncio.sleep(delay)
    logger.info("Order completed", order_id=order_id, trace_id=trace_id)


async def handle_request(request_id: int) -> None:
    """Simulate handling an HTTP request with trace ID propagation."""
    # Set custom trace ID (e.g., from X-Trace-Id header)
    custom_trace = f"req-{request_id:04d}"
    LoggerCore.set_trace_id(custom_trace)

    logger = LoggerCore.get_logger("api")

    logger.info("Request received", request_id=request_id)

    # Call other functions - they inherit the same trace ID
    await authenticate_user(request_id)
    await query_database(request_id)

    logger.info("Request completed", request_id=request_id)


async def authenticate_user(request_id: int) -> None:
    """Simulate auth - inherits trace ID from caller."""
    logger = LoggerCore.get_logger("auth")
    await asyncio.sleep(0.1)
    logger.debug("User authenticated", request_id=request_id)


async def query_database(request_id: int) -> None:
    """Simulate DB query - inherits trace ID from caller."""
    logger = LoggerCore.get_logger("database")
    await asyncio.sleep(0.1)
    logger.debug("Query executed", request_id=request_id)


async def main() -> None:
    """Run examples."""
    print("\n=== Example 1: Concurrent Tasks with Isolated Trace IDs ===\n")

    # Launch 3 concurrent order processing tasks
    # Each will have its own unique trace ID automatically
    tasks = [
        process_order(order_id=101, delay=0.3),
        process_order(order_id=102, delay=0.2),
        process_order(order_id=103, delay=0.4),
    ]

    await asyncio.gather(*tasks)

    print("\n=== Example 2: Request Handling with Custom Trace IDs ===\n")

    # Simulate multiple concurrent HTTP requests
    # Each sets its own trace ID and propagates it through function calls
    requests = [
        handle_request(request_id=1),
        handle_request(request_id=2),
        handle_request(request_id=3),
    ]

    await asyncio.gather(*requests)


if __name__ == "__main__":
    print("=" * 70)
    print("lib_logger Async Trace ID Examples")
    print("=" * 70)
    print("\nDemonstrating how trace IDs work in async contexts:")
    print("- Each concurrent task gets its own unique trace ID")
    print("- Trace IDs are isolated between tasks using contextvars")
    print("- Custom trace IDs can be set (e.g., from HTTP headers)")
    print("- Trace IDs propagate through all function calls in the same context")
    print("=" * 70)

    asyncio.run(main())

    print("\n" + "=" * 70)
    print("Notice how:")
    print("1. Each order had a unique trace ID (8-char hex)")
    print("2. Each request had its custom trace ID (req-XXXX)")
    print("3. All logs within a request/task share the same trace ID")
    print("4. Logs from different tasks are interleaved but distinguishable")
    print("=" * 70)

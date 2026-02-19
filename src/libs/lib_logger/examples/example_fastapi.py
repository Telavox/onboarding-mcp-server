"""Example demonstrating FastAPI integration with unified logging.

This example shows how to configure lib_logger to intercept FastAPI/uvicorn
logs and maintain a consistent logging format across all components.

Run with:
    uv run --package lib_logger python -m examples.example_fastapi

Visit:
    http://localhost:8000/docs
    http://localhost:8000/
    http://localhost:8000/items/42
"""

from contextlib import asynccontextmanager
from typing import Any

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
except ImportError:
    print("FastAPI not installed. Install with: uv add fastapi uvicorn")
    exit(1)

from lib_logger import LoggerCore, configure_fastapi_logging
from lib_logger.adapters import ConsoleAdapter

# Configure logging before creating the app
configure_fastapi_logging(adapters=[ConsoleAdapter(level="INFO")])

logger = LoggerCore.get_logger("fastapi_example")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Application starting up", trace_id=LoggerCore.get_trace_id())
    yield
    logger.info("Application shutting down", trace_id=LoggerCore.get_trace_id())


app = FastAPI(title="lib_logger FastAPI Example", lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with trace ID."""
    # Reset trace ID for each request
    LoggerCore.reset_trace_id()
    trace_id = LoggerCore.get_trace_id()

    logger.info(
        "Request started",
        method=request.method,
        path=request.url.path,
        trace_id=trace_id,
    )

    response = await call_next(request)

    logger.info(
        "Request completed",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        trace_id=trace_id,
    )

    return response


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    logger.info("Root endpoint called")
    return {"message": "Hello from lib_logger + FastAPI!"}


@app.get("/items/{item_id}")
async def get_item(item_id: int) -> dict[str, Any] | JSONResponse:
    """Get an item by ID."""
    logger.debug("Fetching item", item_id=item_id)

    if item_id == 0:
        logger.warning("Invalid item ID", item_id=item_id)
        return JSONResponse(
            status_code=400, content={"error": "Item ID must be greater than 0"}
        )

    # Simulate database query
    logger.info("Item found", item_id=item_id)
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "trace_id": LoggerCore.get_trace_id(),
    }


@app.post("/items")
async def create_item(item: dict[str, Any]) -> dict[str, Any]:
    """Create a new item."""
    logger.info("Creating new item", data=item)

    # Simulate some processing
    logger.debug("Validating item data")
    logger.debug("Saving to database")

    logger.info("Item created successfully", item_id=123)
    return {"item_id": 123, "created": True}


@app.get("/error")
async def trigger_error() -> None:
    """Endpoint that triggers an error."""
    logger.warning("About to trigger an error")
    raise ValueError("This is a test error")


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle ValueError exceptions."""
    logger.error(
        "ValueError occurred",
        error=str(exc),
        path=request.url.path,
        trace_id=LoggerCore.get_trace_id(),
    )
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "trace_id": LoggerCore.get_trace_id()},
    )


if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        print("uvicorn not installed. Install with: uv add uvicorn")
        exit(1)

    logger.info("Starting FastAPI server on http://localhost:8000")
    logger.info("Visit http://localhost:8000/docs for interactive API documentation")

    # Note: uvicorn logs will also go through lib_logger!
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)

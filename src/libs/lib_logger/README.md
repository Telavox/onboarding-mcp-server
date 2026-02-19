# lib_logger

Advanced Python logging library with pluggable adapters, async-safe trace IDs, and standard library integration.

## Features

- **Multiple Output Adapters**: Console, JSON, Google Cloud Logging
- **Async-Safe Trace IDs**: Using `contextvars` for proper async isolation
- **FastAPI/Uvicorn Integration**: Intercept standard library logging
- **Backward Compatible**: Drop-in replacement for the original `CustomLogger`
- **Type-Safe**: Full type hints and `py.typed` marker
- **Zero Configuration**: Works out of the box with sensible defaults

## Installation

```bash
# In workspace projects
uv add lib_logger --source workspace

# Standalone installation (if published to PyPI)
pip install lib_logger
```

## Quick Start

### Basic Usage (Backward Compatible)

```python
from lib_logger import CustomLogger

logger = CustomLogger.get_logger("my_app")

logger.info("Application started")
logger.warning("Connection pool low: {}/10", available)
logger.error("Failed to process request")

# Get trace ID for current context
trace_id = CustomLogger.get_trace_id()
```

### Advanced Usage with Adapters

```python
from lib_logger import configure_logging
from lib_logger.adapters import ConsoleAdapter, JSONAdapter

# Configure multiple outputs
configure_logging(adapters=[
    ConsoleAdapter(level="INFO"),   # Colored console output
    JSONAdapter(level="DEBUG"),     # Structured JSON logs
])

from lib_logger import LoggerCore

logger = LoggerCore.get_logger("service")
logger.info("User logged in", user_id="user_123", ip="192.168.1.1")
```

### FastAPI Integration

```python
from fastapi import FastAPI, Request
from lib_logger import configure_fastapi_logging, LoggerCore
from lib_logger.adapters import ConsoleAdapter

# Configure before creating the app
configure_fastapi_logging(adapters=[ConsoleAdapter(level="INFO")])

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    LoggerCore.reset_trace_id()  # New trace ID per request
    logger = LoggerCore.get_logger("api")

    logger.info("Request started", method=request.method, path=request.url.path)
    response = await call_next(request)
    logger.info("Request completed", status=response.status_code)

    return response
```

Now all uvicorn and FastAPI logs will use the same format as your application logs!

## Output Formats

### Console Adapter (Default)

Colored output to stderr with trace IDs:

```
2026-02-04 16:35:55 | INFO     | 78726fb7 | api | main.py:42 | Request received
2026-02-04 16:35:55 | ERROR    | 78726fb7 | api | main.py:58 | Failed to process
```

### JSON Adapter

Structured JSON output to stdout:

```json
{
  "text": "User logged in",
  "record": {
    "elapsed": { "repr": "0:00:01.234567", "seconds": 1.234567 },
    "exception": null,
    "extra": { "name": "auth", "trace_id": "78726fb7" },
    "file": { "name": "auth.py", "path": "/app/auth.py" },
    "function": "login",
    "level": { "icon": "ℹ️", "name": "INFO", "no": 20 },
    "line": 42,
    "message": "User logged in",
    "module": "auth",
    "name": "auth",
    "process": { "id": 12345, "name": "MainProcess" },
    "thread": { "id": 67890, "name": "MainThread" },
    "time": {
      "repr": "2026-02-04 16:35:55.123456+00:00",
      "timestamp": 1738690555.123456
    }
  }
}
```

### GCP Cloud Logging Adapter

Google Cloud Logging compatible JSON:

```json
{
  "message": "Application started",
  "severity": "INFO",
  "timestamp": "2026-02-04T16:35:55.123456Z",
  "logging.googleapis.com/trace": "78726fb7",
  "logging.googleapis.com/sourceLocation": {
    "file": "main.py",
    "line": "42",
    "function": "startup"
  },
  "name": "app",
  "trace_id": "78726fb7"
}
```

## Available Adapters

### ConsoleAdapter

```python
from lib_logger.adapters import ConsoleAdapter

adapter = ConsoleAdapter(
    level="DEBUG",  # Minimum log level
)
```

### JSONAdapter

```python
from lib_logger.adapters import JSONAdapter

adapter = JSONAdapter(
    level="INFO",
)
```

### GCPAdapter

```python
from lib_logger.adapters import GCPAdapter

adapter = GCPAdapter(
    level="INFO",
)
```

## Async Trace ID Management

Each async context automatically gets its own unique trace ID using `contextvars`:

```python
import asyncio
from lib_logger import LoggerCore

async def process_order(order_id: int):
    LoggerCore.reset_trace_id()  # New trace ID for this task
    logger = LoggerCore.get_logger("orders")

    logger.info("Processing order", order_id=order_id)
    # All logs in this async context share the same trace ID

# Run multiple concurrent tasks - each gets its own trace ID
await asyncio.gather(
    process_order(101),
    process_order(102),
    process_order(103),
)
```

### Custom Trace IDs

Set trace IDs from external sources (e.g., HTTP headers):

```python
from lib_logger import LoggerCore

@app.middleware("http")
async def propagate_trace_id(request: Request, call_next):
    # Get trace ID from header or generate new one
    trace_id = request.headers.get("X-Trace-Id") or LoggerCore.get_trace_id()
    LoggerCore.set_trace_id(trace_id)

    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response
```

## API Reference

### CustomLogger (Legacy API)

Backward-compatible wrapper. Recommended for simple use cases.

```python
from lib_logger import CustomLogger

logger = CustomLogger.get_logger("module_name")
trace_id = CustomLogger.get_trace_id()
CustomLogger.set_trace_id("custom-trace-id")
CustomLogger.reset_trace_id()
```

### LoggerCore (New API)

Advanced API with full adapter support.

```python
from lib_logger import LoggerCore

# Get logger
logger = LoggerCore.get_logger("module_name")

# Trace ID management
trace_id = LoggerCore.get_trace_id()
LoggerCore.set_trace_id("custom-trace-id")
LoggerCore.reset_trace_id()

# Configuration info
is_configured = LoggerCore.is_configured()
adapters = LoggerCore.get_adapters()
```

### Configuration Functions

```python
from lib_logger import configure_logging, configure_fastapi_logging, reset_logging

# General configuration
configure_logging(
    adapters=[ConsoleAdapter()],
    intercept_stdlib=True,
    stdlib_loggers=["uvicorn", "fastapi", "sqlalchemy"]
)

# FastAPI-specific configuration
configure_fastapi_logging(
    adapters=[ConsoleAdapter(), JSONAdapter()]
)

# Reset configuration (useful for testing)
reset_logging()
```

### InterceptHandler

For custom standard library logging integration:

```python
import logging
from lib_logger import InterceptHandler

# Replace logging handler
logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)

# Or for specific loggers
logging.getLogger("uvicorn").handlers = [InterceptHandler()]
```

## Examples

Run the included examples:

```bash
# Basic usage
uv run --package lib_logger python -m examples.example

# Multiple adapters
uv run --package  lib_logger python -m examples.example_adapters

# Async trace IDs
uv run --package lib_logger python -m examples.example_async

# FastAPI integration
uv run --package lib_logger python -m examples.example_fastapi
```

## Testing

```bash
cd src/libs/lib_logger
uv run pytest
```

## Best Practices

### 1. Configure Once at Startup

```python
# main.py or __init__.py
from lib_logger import configure_logging
from lib_logger.adapters import ConsoleAdapter

configure_logging(adapters=[ConsoleAdapter(level="INFO")])
```

### 2. Use Named Loggers

```python
class UserService:
    def __init__(self):
        self.logger = LoggerCore.get_logger(self.__class__.__name__)

    def create_user(self, email: str):
        self.logger.info("Creating user", email=email)
```

### 3. Reset Trace IDs for New Contexts

```python
@app.middleware("http")
async def reset_trace_per_request(request: Request, call_next):
    LoggerCore.reset_trace_id()  # Fresh trace ID per request
    response = await call_next(request)
    return response
```

### 4. Use Multiple Adapters for Production

```python
configure_logging(adapters=[
    ConsoleAdapter(level="INFO"),    # Human-readable for local dev
    JSONAdapter(level="DEBUG"),      # Structured logs for aggregation
    GCPAdapter(level="WARNING"),     # Cloud Logging for alerts
])
```

## Migration Guide

### From Standard Logging

```python
# Before
import logging
logger = logging.getLogger(__name__)
logger.info("Hello")

# After
from lib_logger import LoggerCore
logger = LoggerCore.get_logger(__name__)
logger.info("Hello")
```

### From Old CustomLogger

No changes needed! Code continues to work:

```python
from lib_logger import CustomLogger

logger = CustomLogger.get_logger("app")
logger.info("Still works!")
```

### Adding FastAPI Integration

```python
# Before
from fastapi import FastAPI
app = FastAPI()

# After
from fastapi import FastAPI
from lib_logger import configure_fastapi_logging

configure_fastapi_logging()  # One line!
app = FastAPI()
```

## Requirements

- Python 3.13+
- loguru >= 0.7.0

## License

MIT

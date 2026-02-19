import json

from fastmcp import Context, FastMCP
from lib_logger import LoggerCore
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Debug")


@mcp.tool(
    name="log_request",
    description="Log and return the request object received by the MCP server, including the API key for debugging purposes.",
    tags={"debug", "logging"},
)
def log_request(ctx: Context) -> str:
    """
    Log and return the request object received by the MCP server.

    Returns:
        A formatted JSON string of the received request
    """
    api_key = get_api_key(ctx)
    logger.info("Retrieved request context for debug tool")

    return json.dumps(
        {"apiKey": api_key},
        indent=2,
    )

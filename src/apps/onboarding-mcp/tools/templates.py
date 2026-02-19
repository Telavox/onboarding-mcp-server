import json

import httpx
from lib_logger import LoggerCore
from fastmcp import Context, FastMCP
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Templates")


@mcp.tool(
    name="list_templates",
    description="Retrieves a list of available configuration templates from the Telavox CAPI used for predefined settings.",
    tags={"templates", "configuration"},
)
def list_templates(ctx: Context) -> str:
    """
    Retrieve available configuration templates.
    """
    api_key = get_api_key(ctx)

    response = httpx.get(
        "https://home.telavox.se/api/capi/v1/templates",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    if isinstance(data, list):
        count = len(data)
    elif isinstance(data, dict) and isinstance(data.get("data"), list):
        count = len(data["data"])
    else:
        count = 1

    logger.info(f"Retrieved {count} templates from Telavox CAPI")

    return json.dumps(data, indent=2)

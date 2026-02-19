import json

import httpx
from lib_logger import LoggerCore
from fastmcp import Context, FastMCP
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Queues")


@mcp.tool(
    name="list_queues",
    description="Retrieves a comprehensive list of all call queues configured within the Telavox system.",
    tags={"queues", "pbx"},
)
def list_queues(ctx: Context) -> str:
    """
    Retrieve all call queues from Telavox.
    """
    api_key = get_api_key(ctx)

    response = httpx.get(
        "https://home.telavox.se/api/capi/v1/extensions/pbx/queues",
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

    logger.info(f"Retrieved {count} queues from Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="add_queue_members",
    description="Assigns new members to a specific PBX call queue with member objects defining who should answer calls.",
    tags={"queues", "members", "pbx"},
)
def add_queue_members(ctx: Context, extension: str, body: list[dict]) -> str:
    """
    Add members to a PBX call queue.

    Args:
        extension: The extension identifier of the target PBX queue
        body: An array of member objects defining the extensions to be added to the queue
    """
    api_key = get_api_key(ctx)

    response = httpx.post(
        f"https://home.telavox.se/api/capi/v1/extensions/pbx/queues/{extension}/members",
        headers={"Authorization": f"Bearer {api_key}"},
        json=body,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    logger.info(f"Added {len(body)} queue members in Telavox CAPI")

    return json.dumps(data, indent=2)

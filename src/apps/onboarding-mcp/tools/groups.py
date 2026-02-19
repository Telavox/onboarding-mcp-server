import json

import httpx
from lib_logger import LoggerCore
from fastmcp import Context, FastMCP
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Groups")


@mcp.tool(
    name="list_groups",
    description="Retrieves a list of all groups (such as queues or ring groups) configured within the Telavox system.",
    tags={"groups", "routing"},
)
def list_groups(ctx: Context) -> str:
    """
    Retrieve a list of all groups from the Telavox CAPI.
    """
    api_key = get_api_key(ctx)

    response = httpx.get(
        "https://home.telavox.se/api/capi/v1/groups",
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

    logger.info(f"Retrieved {count} groups from Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="update_group_members",
    description="Updates the membership list for a specific group (such as a queue or ring group) in the Telavox CAPI.",
    tags={"groups", "members", "update"},
)
def update_group_members(ctx: Context, group_key: str, member_keys: str) -> str:
    """
    Update the membership list for a specific group.

    Args:
        group_key: The unique identifier for the group to be updated
        member_keys: A comma-separated list of extension keys to be assigned as members
    """
    api_key = get_api_key(ctx)

    response = httpx.put(
        f"https://home.telavox.se/api/capi/v1/groups/{group_key}/members",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"memberKeys": member_keys},
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    member_count = len([key for key in member_keys.split(",") if key.strip()])
    logger.info(f"Updated {member_count} group members in Telavox CAPI")

    return json.dumps(data, indent=2)

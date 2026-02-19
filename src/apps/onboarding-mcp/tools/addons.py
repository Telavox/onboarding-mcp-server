import json

import httpx
from lib_logger import LoggerCore
from fastmcp import Context, FastMCP
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Add-ons")


@mcp.tool(
    name="get_available_addons",
    description="Retrieves a list of compatible and available add-on products for a specific user extension from the Telavox CAPI.",
    tags={"addons", "assortment"},
)
def get_available_addons(ctx: Context, user: str) -> str:
    """
    Retrieve available add-ons for a user extension.

    Args:
        user: The unique identifier or extension key (e.g., extension-7422411) of the user
    """
    api_key = get_api_key(ctx)

    response = httpx.get(
        f"https://home.telavox.se/api/capi/v1/assortment/addons/{user}",
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

    logger.info(f"Retrieved {count} add-ons for user {user} from Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="purchase_addon",
    description="Executes the purchase and assignment of a specific add-on product to a user extension.",
    tags={"addons", "purchase"},
)
def purchase_addon(ctx: Context, user: str, assortment_item: str) -> str:
    """
    Purchase and assign an add-on to a user.

    Args:
        user: The unique identifier or extension key of the user
        assortment_item: The unique key of the add-on product to be purchased
    """
    api_key = get_api_key(ctx)

    response = httpx.post(
        f"https://home.telavox.se/api/capi/v1/products/addons/{user}/{assortment_item}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    logger.info(f"Purchased add-on {assortment_item} for user {user} in Telavox CAPI")

    return json.dumps(data, indent=2)

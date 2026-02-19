import json

import httpx
from lib_logger import LoggerCore
from fastmcp import Context, FastMCP
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Invoice Places")


@mcp.tool(
    name="list_invoice_places",
    description="Retrieves a list of valid invoice places (billing locations) for a specific country from the Telavox CAPI.",
    tags={"invoice", "billing"},
)
def list_invoice_places(ctx: Context, country_code: str) -> str:
    """
    Retrieve invoice places for a specific country.

    Args:
        country_code: The ISO country code (e.g., SE) to filter the billing locations
    """
    api_key = get_api_key(ctx)

    response = httpx.get(
        f"https://home.telavox.se/api/capi/v1/invoice-places/country-{country_code}",
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

    logger.info(f"Retrieved {count} invoice places from Telavox CAPI")

    return json.dumps(data, indent=2)

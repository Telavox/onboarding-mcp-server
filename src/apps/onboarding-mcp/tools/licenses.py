import json

import httpx
from lib_logger import LoggerCore
from fastmcp import Context, FastMCP
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Licenses")


@mcp.tool(
    name="get_user_licenses",
    description="Retrieves available user licenses from Telavox CAPI with regional pricing based on geography and currency.",
    tags={"licenses", "assortment"},
)
def get_user_licenses(ctx: Context, country_code: str, currency_code: str) -> str:
    """
    Retrieve available user licenses from Telavox CAPI.

    Args:
        country_code: ISO country code (e.g., SE)
        currency_code: Currency code (e.g., SEK)
    """
    api_key = get_api_key(ctx)

    url = (
        "https://home.telavox.se/api/capi/v1/assortment/"
        f"country-{country_code}/currency-{currency_code}/user-licenses"
    )
    response = httpx.get(
        url,
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

    logger.info(f"Retrieved {count} user licenses from Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="purchase_user_licenses",
    description="Executes a purchase of specific user licenses through the Telavox CAPI with optional invoice placement and quantity specification.",
    tags={"licenses", "purchase"},
)
def purchase_user_licenses(
    ctx: Context,
    country_code: str,
    currency_code: str,
    assortment_key: str,
    invoice_place: str | None = None,
    quantity: int | None = None,
) -> str:
    """
    Purchase user licenses via Telavox CAPI.

    Args:
        country_code: ISO country code (e.g., SE)
        currency_code: Currency code (e.g., SEK)
        assortment_key: The unique identifier for the license type
        invoice_place: Specific billing location identifier (optional)
        quantity: Number of licenses to purchase (defaults to 1)
    """
    api_key = get_api_key(ctx)

    url = (
        "https://home.telavox.se/api/capi/v1/products/user-licenses/"
        f"country-{country_code}/currency-{currency_code}/{assortment_key}"
    )

    params: dict[str, str | int] = {}
    if invoice_place is not None:
        params["invoice_place"] = invoice_place
    if quantity is not None:
        params["quantity"] = quantity

    response = httpx.post(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        params=params or None,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    purchased_quantity = quantity if quantity is not None else 1
    logger.info(f"Purchased {purchased_quantity} user licenses from Telavox CAPI")

    return json.dumps(data, indent=2)

import json

import httpx
from lib_logger import LoggerCore
from fastmcp import Context, FastMCP
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Phone Numbers")


@mcp.tool(
    name="list_available_reserved_phone_numbers",
    description="Retrieves a paginated list of available reserved phone numbers from the Telavox CAPI for a specific country.",
    tags={"phone_numbers", "reserved"},
)
def list_available_reserved_phone_numbers(
    ctx: Context,
    country_code: str,
    page_size: int | None = None,
    page_number: int | None = None,
) -> str:
    """
    List available reserved phone numbers for a country.

    Args:
        country_code: ISO country code used to filter the numbers (e.g., SE)
        page_size: The number of results to return per page (defaults to 50)
        page_number: The specific page index to retrieve (defaults to 0)
    """
    api_key = get_api_key(ctx)

    params: dict[str, str | int] = {"country": f"country-{country_code}"}
    params["pageSize"] = page_size if page_size is not None else 50
    params["pageNumber"] = page_number if page_number is not None else 0

    response = httpx.get(
        "https://home.telavox.se/api/capi/v1/reserved-phone-numbers/available",
        headers={"Authorization": f"Bearer {api_key}"},
        params=params,
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

    logger.info(f"Retrieved {count} reserved phone numbers from Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="purchase_phone_number",
    description="Purchases one or multiple phone numbers from the reserved inventory and assigns them to the organization's account.",
    tags={"phone_numbers", "purchase"},
)
def purchase_phone_number(
    ctx: Context,
    body: list[dict],
    invoice_place: str | None = None,
) -> str:
    """
    Purchase reserved phone numbers.

    This endpoint requires a JSON body with one or more phone number objects.
    The tool supports sending that body directly.

    Args:
        body: An array of objects containing number details (e.g., e164Number, country, usages, key)
        invoice_place: The specific billing location identifier (optional)
    """
    api_key = get_api_key(ctx)

    params: dict[str, str] = {}
    if invoice_place is not None:
        params["invoiceplace"] = invoice_place

    response = httpx.post(
        "https://home.telavox.se/api/capi/v1/reserved-phone-numbers",
        headers={"Authorization": f"Bearer {api_key}"},
        params=params or None,
        json=body,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    logger.info(f"Purchased {len(body)} phone numbers from Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="port_phone_number",
    description="Initiates the porting process to transfer an existing phone number from another operator to Telavox.",
    tags={"phone_numbers", "porting"},
)
def port_phone_number(ctx: Context, phone_number: str, body: dict) -> str:
    """
    Initiate a porting request for a phone number.

    Number Porting
    To port a number, use the following endpoint (not found in Telavox's official
    documentation):
    https://home.telavox.se/api/capi/v1/portings/?startE164Number=%2B46XXXX
    The number must be in E.164 format, including country code, with "+" as "%2B".
    Replace XXXX with the actual number. Example: %2B46739983281 for +46739983281.

    Args:
        phone_number: The phone number to be ported in E.164 format.
            The API expects the value to be passed as the startE164Number query
            parameter. The client will URL-encode the '+' automatically.
        body: A JSON object containing porting details such as preferredPortingDate, orgNumber, and the requested state
    """
    api_key = get_api_key(ctx)

    response = httpx.post(
        "https://home.telavox.se/api/capi/v1/portings",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"startE164Number": phone_number},
        json=body,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    logger.info(f"Started porting request for {phone_number} via Telavox CAPI")

    return json.dumps(data, indent=2)

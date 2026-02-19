import json

import httpx
from lib_logger import LoggerCore
from fastmcp import Context, FastMCP
from utils import get_api_key

logger = LoggerCore.get_logger(__name__)

mcp = FastMCP("Users")


@mcp.tool(
    name="list_users",
    description="Retrieves a list of user extensions from the Telavox CAPI. Can be filtered by phone number or invoice placement.",
    tags={"users", "extensions"},
)
def list_users(
    ctx: Context,
    number: str | None = None,
    invoice_place: str | None = None,
) -> str:
    """
    Retrieve a list of user extensions from Telavox CAPI.

    Args:
        number: Filter the list by a specific phone number (optional)
        invoice_place: Filter the list by a specific billing location identifier (optional)
    """
    api_key = get_api_key(ctx)

    params: dict[str, str] = {}
    if number is not None:
        params["number"] = number
    if invoice_place is not None:
        params["invoice_place"] = invoice_place

    response = httpx.get(
        "https://home.telavox.se/api/capi/v1/extensions/users",
        headers={"Authorization": f"Bearer {api_key}"},
        params=params or None,
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

    logger.info(f"Retrieved {count} users from Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="create_user",
    description="Creates a new user extension within the Telavox system with configuration options for region, billing, email, and templates.",
    tags={"users", "extensions", "create"},
)
def create_user(
    ctx: Context,
    country_code: str,
    invoice_place: str | None = None,
    email: str | None = None,
    template: str | None = None,
    confirmation_email: bool | None = None,
) -> str:
    """
    Create a new user extension in Telavox.

    Args:
        country_code: ISO country code used to set the user's region (e.g., SE)
        invoice_place: The specific billing location identifier (optional)
        email: The email address associated with the new user extension (optional)
        template: The identifier for a predefined configuration template (optional)
        confirmation_email: Whether to send a confirmation email to the user (defaults to false)
    """
    api_key = get_api_key(ctx)

    params: dict[str, str | bool] = {"country_code": country_code}
    if invoice_place is not None:
        params["invoice_place"] = invoice_place
    if email is not None:
        params["email"] = email
    if template is not None:
        params["template"] = template
    if confirmation_email is not None:
        params["confirmation_email"] = confirmation_email

    response = httpx.post(
        "https://home.telavox.se/api/capi/v1/extensions/users",
        headers={"Authorization": f"Bearer {api_key}"},
        params=params,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    logger.info("Created user extension in Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="update_user",
    description="Updates an existing user extension's profile and configuration including name, phone numbers, billing location, and license types.",
    tags={"users", "extensions", "update"},
)
def update_user(ctx: Context, user: str, body: dict) -> str:
    """
    Update an existing user extension.

    Args:
        user: The unique identifier or key of the user extension to update
        body: A JSON object containing the user fields to update (e.g., name, fixedNumber, mobileNumber, invoicePlace, licenseType)
    """
    api_key = get_api_key(ctx)

    response = httpx.put(
        f"https://home.telavox.se/api/capi/v1/extensions/users/{user}",
        headers={"Authorization": f"Bearer {api_key}"},
        json=body,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    logger.info(f"Updated user extension {user} in Telavox CAPI")

    return json.dumps(data, indent=2)


@mcp.tool(
    name="get_colleague",
    description="Retrieves detailed contact and profile information for a specific colleague within the Telavox system.",
    tags={"contacts", "colleagues"},
)
def get_colleague(ctx: Context, user: str) -> str:
    """
    Retrieve a colleague profile by user identifier.

    Args:
        user: The unique identifier or key of the colleague/user to retrieve
    """
    api_key = get_api_key(ctx)

    response = httpx.get(
        f"https://home.telavox.se/api/capi/v1/contacts/colleagues/{user}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    logger.info(f"Retrieved colleague profile for {user} from Telavox CAPI")

    return json.dumps(data, indent=2)

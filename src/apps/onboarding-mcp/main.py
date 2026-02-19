import os

from fastmcp import FastMCP
from lib_logger import LoggerCore
from lib_logger.config import configure_logging_from_env

configure_logging_from_env()

from tools import (  # noqa: E402
    addons,
    debug,
    groups,
    invoice_places,
    licenses,
    phone_numbers,
    queues,
    templates,
    users,
)

logger = LoggerCore.get_logger("onboarding-mcp")

mcp = FastMCP("Onboarding MCP Server")

mcp.mount(users.mcp, prefix="users")
mcp.mount(licenses.mcp, prefix="licenses")
mcp.mount(phone_numbers.mcp, prefix="phone_numbers")
mcp.mount(groups.mcp, prefix="groups")
mcp.mount(queues.mcp, prefix="queues")
mcp.mount(addons.mcp, prefix="addons")
mcp.mount(invoice_places.mcp, prefix="invoice_places")
mcp.mount(templates.mcp, prefix="templates")
mcp.mount(debug.mcp, prefix="debug")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    logger.info("Starting onboarding-mcp on port {port}", port=port)
    mcp.run(transport="http", host="0.0.0.0", port=port, path="/mcp")

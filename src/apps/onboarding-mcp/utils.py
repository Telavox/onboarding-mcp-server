from fastmcp import Context
from fastmcp.server.dependencies import get_http_headers


def get_api_key(ctx: Context) -> str:
    if ctx.request_context:
        headers = getattr(ctx.request_context.request, "headers", {})
    else:
        headers = get_http_headers()

    if not headers:
        raise ValueError("No headers found in the request context")

    api_key = headers.get("authorization", None)
    if not api_key:
        raise ValueError("No Authorization header found")

    api_key = api_key.replace("Bearer ", "")

    return api_key

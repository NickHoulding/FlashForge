"""Tools for server diagnostics."""

from typing import Any

from ..instance import mcp
from ..utils import build_success_response


@mcp.tool(description="Health check for MCP server")
def health_check() -> dict[str, Any]:
    """Verify the server is operational."""
    return build_success_response({"status": "healthy"})

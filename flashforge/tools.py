"""All tools for the FlashForge MCP server."""

from fastmcp import tools

from .instance import mcp


@mcp.tool
def save_flashcards(data: dict[str, str]) -> bool:
    """"""
    raise NotImplementedError

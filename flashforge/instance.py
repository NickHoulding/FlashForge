"""FastMCP instance for FlashForge MCP Server.

Creates the global MCP server instance used by all tool modules.
"""

from fastmcp import FastMCP

from .config import Config

mcp: FastMCP = FastMCP(name=Config.SERVER_NAME)

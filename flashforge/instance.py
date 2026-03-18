"""FastMCP instance for FlashForge MCP Server."""

from fastmcp import FastMCP

from .config import Config

mcp: FastMCP = FastMCP(name=Config.SERVER_NAME)

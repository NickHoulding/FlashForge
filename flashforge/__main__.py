"""MCP server entry point - registers all tool modules and runs the server."""

import logging

from . import tools
from .config import Config
from .instance import mcp


def main() -> None:
    """Initialize configuration, logging, and start the MCP server."""
    Config.validate()
    logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
    mcp.run(transport="sse", host=Config.HOST, port=Config.PORT)


if __name__ == "__main__":
    main()

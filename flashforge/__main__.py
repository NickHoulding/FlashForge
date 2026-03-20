"""MCP server entry point - registers all tool modules and runs the server."""

import logging

from . import tools
from .config import Config
from .instance import mcp
from .logging_config import configure_logging


def main() -> None:
    """Initialize configuration, logging, and start the MCP server."""
    configure_logging(
        log_level=Config.LOG_LEVEL,
        log_file=Config.LOG_FILE,
        json_console=Config.LOG_JSON_CONSOLE,
        max_bytes=Config.LOG_MAX_BYTES,
        backup_count=Config.LOG_BACKUP_COUNT,
    )

    logger = logging.getLogger(__name__)
    logger.info("FlashForge MCP server starting")

    Config.validate()

    logger.info("Starting MCP server on stdio transport")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

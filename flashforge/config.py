"""Configuration settings for the FlashForge MCP server."""

import logging
import os


class Config:
    """Global configuration for FlashForge MCP server runtime settings."""

    SERVER_NAME: str = "FlashForge MCP Server"
    """Display name for the MCP server."""

    LOG_LEVEL: int = logging.INFO
    """Logging verbosity level for the MCP server process."""

    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    """Log record format string passed to logging.basicConfig."""

    HOST: str = os.environ.get("HOST", "0.0.0.0")
    """Network interface the MCP server binds to. Override via HOST env var."""

    PORT: int = int(os.environ.get("PORT", "3003"))
    """TCP port the MCP server listens on. Override via PORT env var."""

    @classmethod
    def validate(cls) -> None:
        """Validate all configuration settings.

        Raises:
            ValueError: If any configuration value is invalid or out of range.
        """

        if not isinstance(cls.LOG_LEVEL, int):
            raise ValueError("LOG_LEVEL must be an int")
        if cls.LOG_LEVEL not in (
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ):
            raise ValueError(
                "LOG_LEVEL must be a valid logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
            )

        if not isinstance(cls.LOG_FORMAT, str):
            raise ValueError("LOG_FORMAT must be a string")
        if len(cls.LOG_FORMAT) == 0:
            raise ValueError("LOG_FORMAT cannot be empty")

        if not isinstance(cls.HOST, str):
            raise ValueError("HOST must be a string")
        if len(cls.HOST) == 0:
            raise ValueError("HOST cannot be empty")

        if not isinstance(cls.PORT, int):
            raise ValueError("PORT must be an int")
        if not (1 <= cls.PORT <= 65535):
            raise ValueError("PORT must be between 1 and 65535")

"""Configuration settings for the FlashForge MCP server."""

import logging
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Global configuration for FlashForge MCP server runtime settings."""

    # =============================================================================
    # Ollama Connection
    # =============================================================================

    OLLAMA_MODEL: str = os.environ.get("FLASHCARD_MODEL", "qwen3.5:4b")
    """Model name to use for flashcard generation. Override via FLASHCARD_MODEL env var."""

    SHOULD_THINK: bool = bool(os.environ.get("SHOULD_THINK", "False"))
    """Enable extended reasoning mode during generation. Override via SHOULD_THINK env var."""

    # =============================================================================
    # Flashcard Constraints
    # =============================================================================

    QUESTION_MAX_LEN: int = int(os.environ.get("QUESTION_MAX_LEN", "200"))
    """Maximum character length for flashcard questions. Override via QUESTION_MAX_LEN env var."""

    ANSWER_MAX_LEN: int = int(os.environ.get("ANSWER_MAX_LEN", "500"))
    """Maximum character length for flashcard answers. Override via ANSWER_MAX_LEN env var."""

    MAX_CARDS: int = int(os.environ.get("MAX_CARDS", "50"))
    """Maximum number of flashcards that can be generated in one request. Override via MAX_CARDS env var."""

    TEXT_MAX_LEN: int = int(os.environ.get("TEXT_MAX_LEN", "400"))
    """Maximum character length for input text source material. Override via TEXT_MAX_LEN env var."""

    # =============================================================================
    # Server Metadata
    # =============================================================================

    SERVER_NAME: str = "FlashForge MCP Server"
    """Display name for the MCP server."""

    # =============================================================================
    # Logging
    # =============================================================================

    LOG_LEVEL: int = logging.INFO
    """Logging verbosity level for the MCP server process."""

    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    """Log record format string passed to logging.basicConfig."""

    # =============================================================================
    # Validation
    # =============================================================================

    @classmethod
    def validate(cls) -> None:
        """Validate all configuration settings.

        Raises:
            ValueError: If any configuration value is invalid or out of range.
        """

        # Ollama Connection Validation
        if not isinstance(cls.OLLAMA_MODEL, str):
            raise ValueError("OLLAMA_MODEL must be a string")
        if len(cls.OLLAMA_MODEL) == 0:
            raise ValueError("OLLAMA_MODEL cannot be empty")

        if not isinstance(cls.SHOULD_THINK, bool):
            raise ValueError("SHOULD_THINK must be a boolean")

        # Flashcard Constraints Validation
        if not isinstance(cls.QUESTION_MAX_LEN, int):
            raise ValueError("QUESTION_MAX_LEN must be an int")
        if cls.QUESTION_MAX_LEN <= 0:
            raise ValueError("QUESTION_MAX_LEN must be positive")
        if cls.QUESTION_MAX_LEN > 1000:
            raise ValueError("QUESTION_MAX_LEN cannot exceed 1000 characters")

        if not isinstance(cls.ANSWER_MAX_LEN, int):
            raise ValueError("ANSWER_MAX_LEN must be an int")
        if cls.ANSWER_MAX_LEN <= 0:
            raise ValueError("ANSWER_MAX_LEN must be positive")
        if cls.ANSWER_MAX_LEN > 2000:
            raise ValueError("ANSWER_MAX_LEN cannot exceed 2000 characters")

        if not isinstance(cls.MAX_CARDS, int):
            raise ValueError("MAX_CARDS must be an int")
        if cls.MAX_CARDS <= 0:
            raise ValueError("MAX_CARDS must be positive")
        if cls.MAX_CARDS > 100:
            raise ValueError("MAX_CARDS cannot exceed 100")

        if not isinstance(cls.TEXT_MAX_LEN, int):
            raise ValueError("TEXT_MAX_LEN must be an int")
        if cls.TEXT_MAX_LEN <= 0:
            raise ValueError("TEXT_MAX_LEN must be positive")
        if cls.TEXT_MAX_LEN > 100000:
            raise ValueError("TEXT_MAX_LEN cannot exceed 100000 characters")

        # Server Metadata Validation
        if not isinstance(cls.SERVER_NAME, str):
            raise ValueError("SERVER_NAME must be a string")
        if len(cls.SERVER_NAME) == 0:
            raise ValueError("SERVER_NAME cannot be empty")

        # Logging Validation
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

"""Configuration settings for the FlashForge MCP server."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """Global configuration for FlashForge MCP server runtime settings."""

    # =============================================================================
    # Ollama Connection
    # =============================================================================

    OLLAMA_MODEL: str = os.environ.get("FLASHCARD_MODEL", "qwen3.5:4b")
    """Model name to use for flashcard generation. Override via FLASHCARD_MODEL env var."""

    _SHOULD_THINK_STR: str = os.environ.get("SHOULD_THINK", "False").lower()
    SHOULD_THINK: bool = _SHOULD_THINK_STR in ("true", "True")
    """Enable extended reasoning mode during generation. Override via SHOULD_THINK env var."""

    # =============================================================================
    # VectorForge RAG Connection
    # =============================================================================

    VECTORFORGE_BASE_URL: str = os.environ.get(
        "VECTORFORGE_BASE_URL", "http://localhost:8000"
    )
    """Base URL for the VectorForge RAG service. Override via VECTORFORGE_BASE_URL env var."""

    RAG_TOP_K: int = int(os.environ.get("RAG_TOP_K", "5"))
    """Number of top results to retrieve from VectorForge search. Override via RAG_TOP_K env var."""

    CONTEXT_MAX_LEN: int = int(os.environ.get("CONTEXT_MAX_LEN", "10000"))
    """Maximum character length for concatenated RAG context. Override via CONTEXT_MAX_LEN env var."""

    TIMEOUT: int = 30
    """"""

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
    # File Storage
    # =============================================================================

    OUTPUT_DIR: str = os.environ.get("OUTPUT_DIR", "./output")
    """Directory path for saving flashcard output files. Override via OUTPUT_DIR env var."""

    MAX_FILE_NAME_LEN: int = int(os.environ.get("MAX_FILE_NAME_LEN", "255"))
    """Maximum character length for output file names. Override via MAX_FILE_NAME_LEN env var."""

    # =============================================================================
    # Server Metadata
    # =============================================================================

    SERVER_NAME: str = "FlashForge MCP Server"
    """Display name for the MCP server."""

    # =============================================================================
    # Logging
    # =============================================================================

    _LOG_LEVEL_STR: str = os.environ.get("FF_LOG_LEVEL", "INFO").upper()
    LOG_LEVEL: int = getattr(logging, _LOG_LEVEL_STR, logging.INFO)
    """Logging verbosity level for the MCP server process."""

    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    """Log record format string passed to logging.basicConfig (deprecated, kept for backwards compatibility)."""

    LOG_FILE: str = os.environ.get("FF_LOG_FILE", "./logs/flashforge.log")
    """Path to log file for rotating file handler. Override via FF_LOG_FILE env var."""

    LOG_JSON_CONSOLE: bool = (
        os.environ.get("FF_LOG_JSON_CONSOLE", "false").lower() == "true"
    )
    """Enable JSON logging to console. Override via FF_LOG_JSON_CONSOLE env var."""

    LOG_MAX_TEXT_LEN: int = int(os.environ.get("FF_LOG_MAX_TEXT_LEN", "100"))
    """Maximum character length for text sanitization in logs. Override via FF_LOG_MAX_TEXT_LEN env var."""

    LOG_MAX_BYTES: int = int(os.environ.get("FF_LOG_MAX_BYTES", "10485760"))
    """Maximum size per log file before rotation in bytes (default: 10MB). Override via FF_LOG_MAX_BYTES env var."""

    LOG_BACKUP_COUNT: int = int(os.environ.get("FF_LOG_BACKUP_COUNT", "5"))
    """Number of backup log files to keep during rotation (default: 5). Override via FF_LOG_BACKUP_COUNT env var."""

    # =============================================================================
    # Validation
    # =============================================================================

    @classmethod
    def validate(cls) -> None:
        """Validate all configuration settings.

        Raises:
            ValueError: If any configuration value is invalid or out of range.
        """
        logger.info("Starting configuration validation")

        # Ollama Connection Validation
        logger.debug("Validating OLLAMA_MODEL: %s", cls.OLLAMA_MODEL)
        if not isinstance(cls.OLLAMA_MODEL, str):
            logger.error("OLLAMA_MODEL validation failed: not a string")
            raise ValueError("OLLAMA_MODEL must be a string")
        if len(cls.OLLAMA_MODEL) == 0:
            logger.error("OLLAMA_MODEL validation failed: empty string")
            raise ValueError("OLLAMA_MODEL cannot be empty")

        logger.debug("Validating SHOULD_THINK: %s", cls.SHOULD_THINK)
        if not isinstance(cls.SHOULD_THINK, bool):
            logger.error("SHOULD_THINK validation failed: not a boolean")
            raise ValueError("SHOULD_THINK must be a boolean")

        # VectorForge RAG Connection Validation
        logger.debug("Validating VECTORFORGE_BASE_URL: %s", cls.VECTORFORGE_BASE_URL)
        if not isinstance(cls.VECTORFORGE_BASE_URL, str):
            logger.error("VECTORFORGE_BASE_URL validation failed: not a string")
            raise ValueError("VECTORFORGE_BASE_URL must be a string")
        if len(cls.VECTORFORGE_BASE_URL) == 0:
            logger.error("VECTORFORGE_BASE_URL validation failed: empty string")
            raise ValueError("VECTORFORGE_BASE_URL cannot be empty")
        if not cls.VECTORFORGE_BASE_URL.startswith(("http://", "https://")):
            logger.error("VECTORFORGE_BASE_URL validation failed: invalid protocol")
            raise ValueError("VECTORFORGE_BASE_URL must start with http:// or https://")

        logger.debug("Validating RAG_TOP_K: %d", cls.RAG_TOP_K)
        if not isinstance(cls.RAG_TOP_K, int):
            logger.error("RAG_TOP_K validation failed: not an int")
            raise ValueError("RAG_TOP_K must be an int")
        if cls.RAG_TOP_K <= 0:
            logger.error(
                "RAG_TOP_K validation failed: %d is not positive", cls.RAG_TOP_K
            )
            raise ValueError("RAG_TOP_K must be positive")
        if cls.RAG_TOP_K > 50:
            logger.error("RAG_TOP_K validation failed: %d exceeds 50", cls.RAG_TOP_K)
            raise ValueError("RAG_TOP_K cannot exceed 50")

        logger.debug("Validating CONTEXT_MAX_LEN: %d", cls.CONTEXT_MAX_LEN)
        if not isinstance(cls.CONTEXT_MAX_LEN, int):
            logger.error("CONTEXT_MAX_LEN validation failed: not an int")
            raise ValueError("CONTEXT_MAX_LEN must be an int")
        if cls.CONTEXT_MAX_LEN <= 0:
            logger.error(
                "CONTEXT_MAX_LEN validation failed: %d is not positive",
                cls.CONTEXT_MAX_LEN,
            )
            raise ValueError("CONTEXT_MAX_LEN must be positive")
        if cls.CONTEXT_MAX_LEN > 50000:
            logger.error(
                "CONTEXT_MAX_LEN validation failed: %d exceeds 50000",
                cls.CONTEXT_MAX_LEN,
            )
            raise ValueError("CONTEXT_MAX_LEN cannot exceed 50000 characters")

        # Flashcard Constraints Validation
        logger.debug("Validating QUESTION_MAX_LEN: %d", cls.QUESTION_MAX_LEN)
        if not isinstance(cls.QUESTION_MAX_LEN, int):
            logger.error("QUESTION_MAX_LEN validation failed: not an int")
            raise ValueError("QUESTION_MAX_LEN must be an int")
        if cls.QUESTION_MAX_LEN <= 0:
            logger.error(
                "QUESTION_MAX_LEN validation failed: %d is not positive",
                cls.QUESTION_MAX_LEN,
            )
            raise ValueError("QUESTION_MAX_LEN must be positive")
        if cls.QUESTION_MAX_LEN > 1000:
            logger.error(
                "QUESTION_MAX_LEN validation failed: %d exceeds 1000",
                cls.QUESTION_MAX_LEN,
            )
            raise ValueError("QUESTION_MAX_LEN cannot exceed 1000 characters")

        logger.debug("Validating ANSWER_MAX_LEN: %d", cls.ANSWER_MAX_LEN)
        if not isinstance(cls.ANSWER_MAX_LEN, int):
            logger.error("ANSWER_MAX_LEN validation failed: not an int")
            raise ValueError("ANSWER_MAX_LEN must be an int")
        if cls.ANSWER_MAX_LEN <= 0:
            logger.error(
                "ANSWER_MAX_LEN validation failed: %d is not positive",
                cls.ANSWER_MAX_LEN,
            )
            raise ValueError("ANSWER_MAX_LEN must be positive")
        if cls.ANSWER_MAX_LEN > 2000:
            logger.error(
                "ANSWER_MAX_LEN validation failed: %d exceeds 2000", cls.ANSWER_MAX_LEN
            )
            raise ValueError("ANSWER_MAX_LEN cannot exceed 2000 characters")

        logger.debug("Validating MAX_CARDS: %d", cls.MAX_CARDS)
        if not isinstance(cls.MAX_CARDS, int):
            logger.error("MAX_CARDS validation failed: not an int")
            raise ValueError("MAX_CARDS must be an int")
        if cls.MAX_CARDS <= 0:
            logger.error(
                "MAX_CARDS validation failed: %d is not positive", cls.MAX_CARDS
            )
            raise ValueError("MAX_CARDS must be positive")
        if cls.MAX_CARDS > 100:
            logger.error("MAX_CARDS validation failed: %d exceeds 100", cls.MAX_CARDS)
            raise ValueError("MAX_CARDS cannot exceed 100")

        logger.debug("Validating TEXT_MAX_LEN: %d", cls.TEXT_MAX_LEN)
        if not isinstance(cls.TEXT_MAX_LEN, int):
            logger.error("TEXT_MAX_LEN validation failed: not an int")
            raise ValueError("TEXT_MAX_LEN must be an int")
        if cls.TEXT_MAX_LEN <= 0:
            logger.error(
                "TEXT_MAX_LEN validation failed: %d is not positive", cls.TEXT_MAX_LEN
            )
            raise ValueError("TEXT_MAX_LEN must be positive")
        if cls.TEXT_MAX_LEN > 100000:
            logger.error(
                "TEXT_MAX_LEN validation failed: %d exceeds 100000", cls.TEXT_MAX_LEN
            )
            raise ValueError("TEXT_MAX_LEN cannot exceed 100000 characters")

        # File Storage Validation
        logger.debug("Validating OUTPUT_DIR: %s", cls.OUTPUT_DIR)
        if not isinstance(cls.OUTPUT_DIR, str):
            logger.error("OUTPUT_DIR validation failed: not a string")
            raise ValueError("OUTPUT_DIR must be a string")
        if len(cls.OUTPUT_DIR) == 0:
            logger.error("OUTPUT_DIR validation failed: empty string")
            raise ValueError("OUTPUT_DIR cannot be empty")
        if not Path(cls.OUTPUT_DIR).expanduser().exists():
            logger.error("OUTPUT_DIR validation failed: directory does not exist")
            raise ValueError("OUTPUT_DIR directory must exist")
        if not Path(cls.OUTPUT_DIR).expanduser().is_dir():
            logger.error("OUTPUT_DIR validation failed: not a directory")
            raise ValueError("OUTPUT_DIR must be a valid directory path")

        logger.debug("Validating MAX_FILE_NAME_LEN: %d", cls.MAX_FILE_NAME_LEN)
        if not isinstance(cls.MAX_FILE_NAME_LEN, int):
            logger.error("MAX_FILE_NAME_LEN validation failed: not an integer")
            raise ValueError("MAX_FILE_NAME_LEN must be an integer")
        if cls.MAX_FILE_NAME_LEN <= 0:
            logger.error(
                "MAX_FILE_NAME_LEN validation failed: %d is not positive",
                cls.MAX_FILE_NAME_LEN,
            )
            raise ValueError("MAX_FILE_NAME_LEN must be positive")

        # Server Metadata Validation
        logger.debug("Validating SERVER_NAME: %s", cls.SERVER_NAME)
        if not isinstance(cls.SERVER_NAME, str):
            logger.error("SERVER_NAME validation failed: not a string")
            raise ValueError("SERVER_NAME must be a string")
        if len(cls.SERVER_NAME) == 0:
            logger.error("SERVER_NAME validation failed: empty string")
            raise ValueError("SERVER_NAME cannot be empty")

        # Logging Validation
        logger.debug("Validating LOG_LEVEL: %d", cls.LOG_LEVEL)
        if not isinstance(cls.LOG_LEVEL, int):
            logger.error("LOG_LEVEL validation failed: not an int")
            raise ValueError("LOG_LEVEL must be an int")
        if cls.LOG_LEVEL not in (
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ):
            logger.error("LOG_LEVEL validation failed: invalid level %d", cls.LOG_LEVEL)
            raise ValueError(
                "LOG_LEVEL must be a valid logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
            )

        logger.debug("Validating LOG_FORMAT: %s", cls.LOG_FORMAT[:50] + "...")
        if not isinstance(cls.LOG_FORMAT, str):
            logger.error("LOG_FORMAT validation failed: not a string")
            raise ValueError("LOG_FORMAT must be a string")
        if len(cls.LOG_FORMAT) == 0:
            logger.error("LOG_FORMAT validation failed: empty string")
            raise ValueError("LOG_FORMAT cannot be empty")

        logger.debug("Validating LOG_MAX_BYTES: %d", cls.LOG_MAX_BYTES)
        if not isinstance(cls.LOG_MAX_BYTES, int):
            logger.error("LOG_MAX_BYTES validation failed: not an int")
            raise ValueError("LOG_MAX_BYTES must be an int")
        if cls.LOG_MAX_BYTES <= 0:
            logger.error(
                "LOG_MAX_BYTES validation failed: %d is not positive",
                cls.LOG_MAX_BYTES,
            )
            raise ValueError("LOG_MAX_BYTES must be positive")
        if cls.LOG_MAX_BYTES < 1024:
            logger.error(
                "LOG_MAX_BYTES validation failed: %d is less than 1KB",
                cls.LOG_MAX_BYTES,
            )
            raise ValueError("LOG_MAX_BYTES must be at least 1024 bytes (1KB)")

        logger.debug("Validating LOG_BACKUP_COUNT: %d", cls.LOG_BACKUP_COUNT)
        if not isinstance(cls.LOG_BACKUP_COUNT, int):
            logger.error("LOG_BACKUP_COUNT validation failed: not an int")
            raise ValueError("LOG_BACKUP_COUNT must be an int")
        if cls.LOG_BACKUP_COUNT < 0:
            logger.error(
                "LOG_BACKUP_COUNT validation failed: %d is negative",
                cls.LOG_BACKUP_COUNT,
            )
            raise ValueError("LOG_BACKUP_COUNT must be non-negative")
        if cls.LOG_BACKUP_COUNT > 100:
            logger.error(
                "LOG_BACKUP_COUNT validation failed: %d exceeds 100",
                cls.LOG_BACKUP_COUNT,
            )
            raise ValueError("LOG_BACKUP_COUNT cannot exceed 100")

        logger.info("Configuration validation completed successfully")

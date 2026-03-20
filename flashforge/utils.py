"""Shared response-building helpers for MCP tool handlers."""

from typing import Any

from ollama import chat

from .config import Config
from .models import GenerationResponse
from pathlib import Path
import logging

logger: logging.Logger = logging.getLogger(__name__)

# =============================================================================
# Error Handling Utilities
# =============================================================================


def build_success_response(data: dict[str, Any], **extra_fields: Any) -> dict[str, Any]:
    """Build a standardised success response from an API response dictionary.

    Args:
      data: JSON response dict returned from the FlashForge REST API.
      **extra_fields: Additional key-value pairs to merge into the response.

    Returns:
      Dict with ``success: True`` merged with all data and extra fields.
    """
    return {"success": True, **data, **extra_fields}


def build_error_response(error: Exception, details: Any = None) -> dict[str, Any]:
    """Build a standardised error response.

    Args:
      error: The exception that was caught.
      details: Optional extra context, such as an HTTP status code.

    Returns:
      Dict with ``success: False``, the error message, and optional details.
    """
    response: dict[str, Any] = {
        "success": False,
        "error": str(error),
    }

    if details is not None:
        response["details"] = details

    return response


# =============================================================================
# Flashcard Generation Utilities
# =============================================================================


def _validate_generation_params(text: str, num_cards: int) -> None:
    """Validate input parameters for flashcard generation.

    Args:
        text: Source material to validate.
        num_cards: Number of flashcards to validate.

    Raises:
        ValueError: If text is empty, exceeds TEXT_MAX_LEN, num_cards is
            invalid, or exceeds MAX_CARDS.
    """
    logger.debug(f"Validating generation tool input args")

    if not text:
        logger.error(f"Invalid input argument 'text'")
        raise ValueError(f"Input argument 'text' cannot be empty")
    if len(text) > Config.TEXT_MAX_LEN:
        logger.error(f"Input argument 'text' too long (length: {len(text)})")
        raise ValueError(f"Input text too long ({len(text)})")
    if num_cards <= 0:
        logger.error(f"Input argument 'num_cards' was negative")
        raise ValueError("num_cards must be a positive integer")
    if num_cards > Config.MAX_CARDS:
        logger.error(f"Cannot generate greater than {Config.MAX_CARDS} flashcards at once. Attempted {num_cards}")
        raise ValueError(f"num_cards must not exceed the maximum: {Config.MAX_CARDS}")

    logger.debug("Generation tool input args validated")


def _generate_flashcards_from_messages(
    messages: list[dict[str, Any]],
) -> GenerationResponse:
    """Call the LLM to generate flashcards from provided messages.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.

    Returns:
        GenerationResponse containing the list of generated flashcards.

    Raises:
        ValueError: If the LLM returns empty content or invalid JSON.
    """
    logger.debug("Generating flashcards")

    resp = chat(
        model=Config.OLLAMA_MODEL,
        think=Config.SHOULD_THINK,
        format=GenerationResponse.model_json_schema(),
        messages=messages,
    )

    if not resp.message.content:
        logger.error("No content was generated")
        raise ValueError("Did not generate any content")

    logger.debug("Validating generation")
    generation: GenerationResponse = GenerationResponse.model_validate_json(
        resp.message.content or ""
    )
    logger.debug("Generation validated")

    return generation


def _validate_safe_path(base_dir: Path, user_path: str) -> Path:
    """Validate and resolve a user-provided path within a safe base directory.

    Prevents path traversal attacks by ensuring the resolved path stays within
    the base directory. Expands user home directory (~) and resolves symlinks.

    Args:
        base_dir: The base directory that paths must stay within.
        user_path: User-provided path string, may include ~, .., or symlinks.

    Returns:
        Resolved absolute Path object guaranteed to be within base_dir.

    Raises:
        ValueError: If the resolved path escapes base_dir (path traversal attempt).
    """
    base = base_dir.expanduser().resolve()
    full_path = (base / user_path).resolve()

    if not str(full_path).startswith(str(base)):
        raise ValueError(f"Path traversal attempted: {user_path}")

    return full_path

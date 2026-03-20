"""Shared response-building helpers for MCP tool handlers."""

import logging
from pathlib import Path
from typing import Any

from ollama import chat

from .config import Config
from .logging_config import _sanitize_text_for_logging
from .models import GenerationResponse

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
    logger.debug(
        "Entering _validate_generation_params: text_len=%d, num_cards=%d",
        len(text),
        num_cards,
    )

    if not text:
        logger.error("Invalid input argument 'text': cannot be empty")
        raise ValueError("Input argument 'text' cannot be empty")
    if len(text) > Config.TEXT_MAX_LEN:
        logger.error(
            "Input argument 'text' too long: %d chars (max: %d)",
            len(text),
            Config.TEXT_MAX_LEN,
        )
        raise ValueError("Input text too long (%d)" % len(text))
    if num_cards <= 0:
        logger.error("Input argument 'num_cards' was negative or zero: %d", num_cards)
        raise ValueError("num_cards must be a positive integer")
    if num_cards > Config.MAX_CARDS:
        logger.error(
            "num_cards exceeds maximum: requested=%d, max=%d",
            num_cards,
            Config.MAX_CARDS,
        )
        raise ValueError("num_cards must not exceed the maximum: %d" % Config.MAX_CARDS)

    logger.debug("Exiting _validate_generation_params: validation passed")


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
    logger.debug(
        "Entering _generate_flashcards_from_messages: %d messages", len(messages)
    )

    resp = chat(
        model=Config.OLLAMA_MODEL,
        think=Config.SHOULD_THINK,
        format=GenerationResponse.model_json_schema(),
        messages=messages,
    )

    if not resp.message.content:
        logger.error("LLM returned empty content")
        raise ValueError("Did not generate any content")

    generation: GenerationResponse = GenerationResponse.model_validate_json(
        resp.message.content or ""
    )

    logger.debug(
        "Exiting _generate_flashcards_from_messages: generated %d flashcards",
        len(generation.flashcards),
    )

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
    logger.debug("Validating safe path: base_dir=%s, user_path=%s", base_dir, user_path)

    base = base_dir.expanduser().resolve()
    full_path = (base / user_path).resolve()

    if not str(full_path).startswith(str(base)):
        logger.error(
            "Path traversal attempted: user_path=%s, resolved=%s", user_path, full_path
        )
        raise ValueError("Path traversal attempted: %s" % user_path)

    logger.debug("Safe path validated: %s", full_path)
    return full_path

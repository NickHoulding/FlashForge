"""Shared response-building helpers for MCP tool handlers."""

from typing import Any

from ollama import chat

from .config import Config
from .models import GenerationResponse

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
# Flaschard Generation Utilities
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
    if not text:
        raise ValueError(f"Input text too short ({len(text)})")
    if len(text) > Config.TEXT_MAX_LEN:
        raise ValueError(f"Input text too long ({len(text)})")
    if num_cards <= 0:
        raise ValueError("num_cards must be a positive integer")
    if num_cards > Config.MAX_CARDS:
        raise ValueError(f"num_cards must not exceed the maximum: {Config.MAX_CARDS}")


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
    resp = chat(
        model=Config.OLLAMA_MODEL,
        think=Config.SHOULD_THINK,
        format=GenerationResponse.model_json_schema(),
        messages=messages,
    )

    if not resp.message.content:
        raise ValueError("Did not generate any content")

    generation: GenerationResponse = GenerationResponse.model_validate_json(
        resp.message.content or ""
    )

    return generation

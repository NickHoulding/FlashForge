"""MCP tool implementations for the FlashForge flashcard generation server.

Contains generation tools and persistence tools for AI-powered flashcard creation.
"""

import json
import os
from typing import Any

import pandas as pd
import requests
from fastmcp import tools
from ollama import chat

from .config import Config
from .errors import handle_tool_errors
from .instance import mcp
from .models import GenerationResponse
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .utils import build_success_response

# =============================================================================
# Generation Tools
# =============================================================================


@mcp.tool(description="Generate flashcards from provided text using AI")
@handle_tool_errors
def generate_flashcards(text: str, num_cards: int) -> dict[str, Any]:
    """Generate study flashcards from source material using an LLM.

    Takes input text and generates a specified number of question-answer
    flashcard pairs suitable for spaced repetition study systems.

    Args:
        text: Source material to extract flashcard Q&A pairs from.
        num_cards: Number of flashcards to generate (1 to MAX_CARDS).

    Returns:
        Success response dict containing a list of generated flashcards,
        each with 'question' and 'answer' fields.

    Raises:
        ValueError: If text is empty, exceeds TEXT_MAX_LEN, num_cards is
            invalid, or generation produces invalid output.
    """
    if not text:
        raise ValueError(f"Input text too short ({len(text)})")
    if len(text) > Config.TEXT_MAX_LEN:
        raise ValueError(f"Input text too long ({len(text)})")
    if num_cards <= 0:
        raise ValueError("num_cards must be a positive integer")
    if num_cards > Config.MAX_CARDS:
        raise ValueError(f"num_cards must not exceed the maximum: {Config.MAX_CARDS}")

    resp = chat(
        model=Config.OLLAMA_MODEL,
        think=Config.SHOULD_THINK,
        format=GenerationResponse.model_json_schema(),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(text, num_cards)},
        ],
    )

    if not resp.message.content:
        raise ValueError("Did not generate any content")

    generation: GenerationResponse = GenerationResponse.model_validate_json(
        resp.message.content or ""
    )

    if len(generation.flashcards) > num_cards:
        raise ValueError(
            f"Generated too many flashcards ({len(generation.flashcards)}) when only {num_cards} were requested"
        )

    return build_success_response(generation.model_dump())


@mcp.tool(description="Generate flashcards from a topic name using AI research")
def generate_flashcards_from_topic(topic: str) -> dict[str, Any]:
    """Generate flashcards by having the LLM research a topic autonomously.

    Args:
        topic: Subject or topic name to generate flashcards about.

    Returns:
        Success response dict containing generated flashcards.

    Raises:
        NotImplementedError: This tool is not yet implemented.
    """
    raise NotImplementedError


# =============================================================================
# Persistence Tools
# =============================================================================


@mcp.tool(description="Save flashcards to persistent storage")
def save_flashcards(flashcards: dict[str, str]) -> dict[str, Any]:
    """Persist flashcards to the configured storage backend.

    Args:
        flashcards: Dictionary mapping flashcard IDs to their data.

    Returns:
        Success response with storage confirmation details.

    Raises:
        NotImplementedError: This tool is not yet implemented.
    """
    raise NotImplementedError


@mcp.tool(description="Export flashcards to CSV format")
def export_flashcards_csv(file_path: str) -> dict[str, Any]:
    """Export flashcards to a CSV file for external use.

    Args:
        file_path: Destination path for the CSV file.

    Returns:
        Success response with export details and file path.

    Raises:
        NotImplementedError: This tool is not yet implemented.
    """
    raise NotImplementedError

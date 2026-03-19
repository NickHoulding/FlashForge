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
from requests import HTTPError

from .config import Config
from .errors import handle_tool_errors
from .instance import mcp
from .models import GenerationResponse
from .prompts import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_RAG,
    build_user_prompt,
    build_user_prompt_rag,
)
from .utils import _get_flashcards, _validate_generation_params, build_success_response

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
    _validate_generation_params(text=text, num_cards=num_cards)

    generation: GenerationResponse = _get_flashcards(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(text, num_cards)},
        ]
    )

    if len(generation.flashcards) > num_cards:
        raise ValueError(
            f"Generated too many flashcards ({len(generation.flashcards)}) when only {num_cards} were requested"
        )

    return build_success_response(generation.model_dump())


@mcp.tool(description="Generate flashcards from a topic name using AI research")
@handle_tool_errors
def generate_flashcards_from_topic(topic: str, num_cards: int) -> dict[str, Any]:
    """Generate flashcards by having the LLM research a topic autonomously.

    Args:
        topic: Subject or topic name to generate flashcards about.

    Returns:
        Success response dict containing generated flashcards.

    Raises:
        NotImplementedError: This tool is not yet implemented.
    """
    _validate_generation_params(text=topic, num_cards=num_cards)

    response = requests.post(
        url=f"{Config.VECTORFORGE_BASE_URL}/collections/flashforge/search",
        params={"query": topic, "top_k": Config.RAG_TOP_K},
    )

    if response.status_code != 200:
        error = HTTPError(
            f"VectorForge search failed with status {response.status_code}: {response.text}"
        )
        error.response = response
        raise error
    if not response.content:
        error = HTTPError("VectorForge returned empty response")
        error.response = response
        raise error

    data = response.json()
    results: list[dict[str, Any]] = data.get("results", [])

    if not results:
        raise ValueError(f"No context found for topic: {topic}")

    context_chunks: list[str] = []
    for result in results:
        if "content" in result and result["content"]:
            content = result["content"]
            if isinstance(content, str):
                context_chunks.append(content)

    if not context_chunks:
        raise ValueError(f"No valid content retrieved for topic: {topic}")

    context = "\n\n".join(context_chunks)

    if len(context) > Config.CONTEXT_MAX_LEN:
        context = context[: Config.CONTEXT_MAX_LEN] + "..."

    generation: GenerationResponse = _get_flashcards(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_RAG},
            {
                "role": "user",
                "content": build_user_prompt_rag(topic, context, num_cards),
            },
        ],
    )

    if len(generation.flashcards) == 0:
        raise ValueError(f"Failed to generate any flashcards")

    return build_success_response(generation.model_dump())


# =============================================================================
# Persistence Tools
# =============================================================================


@mcp.tool(description="Save flashcards to persistent storage")
@handle_tool_errors
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
@handle_tool_errors
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

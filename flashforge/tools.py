"""MCP tool implementations for the FlashForge flashcard generation server.

Contains generation tools and persistence tools for AI-powered flashcard creation.
"""

import json
from pathlib import Path
from typing import Any

import pandas as pd
import requests
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
from .utils import (
    _generate_flashcards_from_messages,
    _validate_generation_params,
    _validate_safe_path,
    build_success_response,
)
import logging

logger: logging.Logger = logging.getLogger(__name__)

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

    generation: GenerationResponse = _generate_flashcards_from_messages(
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
        timeout=Config.TIMEOUT
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

    generation: GenerationResponse = _generate_flashcards_from_messages(
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
def save_flashcards(flashcards: dict[str, str], file_name: str) -> dict[str, Any]:
    """Save flashcards to a JSON file in the configured output directory.

    Args:
        flashcards: Dictionary mapping flashcard IDs to their data.
        file_name: Name of the output file (without directory path).

    Returns:
        Success response dict with confirmation message and save location.

    Raises:
        ValueError: If flashcards dict is empty, file_name is empty or invalid,
            or file_name exceeds MAX_FILE_NAME_LEN.
        OSError: If file cannot be created or written to the output directory.
    """
    if len(flashcards) == 0:
        raise ValueError("0 flascards were provided - nothing to save")
    if len(file_name) == 0:
        raise ValueError("file_name cannot be empty")
    if len(file_name) > Config.MAX_FILE_NAME_LEN:
        raise ValueError(f"file_name too long ({len(file_name)})")

    file_path: Path = _validate_safe_path(
        base_dir=Path(Config.OUTPUT_DIR),
        user_path=file_name
    )

    try:
        with open(file_path, "w") as f:
            json.dump(flashcards, f, indent=2)
    except OSError as e:
        raise OSError(f"Failed to write flashcards to {file_path}: {e.strerror}") from e

    return build_success_response(
        {"message": f"Flashcards successfully saved to: {file_path}"}
    )


@mcp.tool(description="Export flashcards to CSV format")
@handle_tool_errors
def export_flashcards_csv(
    input_path: str, output_path: str | None = None
) -> dict[str, Any]:
    """Export flashcards from a JSON file to CSV format.

    Reads a JSON file containing flashcards and converts it to a CSV file
    with columns for each flashcard field (question, answer, etc.).

    Args:
        input_path: Path to the input JSON file containing flashcards.
        output_path: Optional path for the output CSV file. If not provided,
            uses the same path as input_path but with .csv extension.

    Returns:
        Success response dict with confirmation message.

    Raises:
        FileNotFoundError: If input_path does not exist.
        OSError: If input file cannot be read, or if the output file cannot be written.
    """
    in_path: Path = Path(input_path).expanduser()
    out_path: Path = (
        Path(output_path).expanduser() if output_path else in_path.with_suffix(".csv")
    )

    try:
        with open(in_path, "r") as f:
            data: dict[str, str] = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"JSON File not found at location: '{in_path}'") from e
    except OSError as e:
        raise OSError(f"Failed to read flashcards from {in_path}: {e.strerror}") from e

    df: pd.DataFrame = pd.DataFrame(data.get("flashcards", []))
    df.to_csv(out_path, index=False)

    return build_success_response(
        {"message": f"Flashcards successfully converted to CSV: {out_path}"}
    )

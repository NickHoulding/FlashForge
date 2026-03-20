"""MCP tool implementations for the FlashForge flashcard generation server.

Contains generation tools and persistence tools for AI-powered flashcard creation.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from requests import HTTPError

from .config import Config
from .errors import handle_tool_errors
from .instance import mcp
from .logging_config import _sanitize_text_for_logging
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
    logger.debug(
        "Entering generate_flashcards: text_len=%d, num_cards=%d, text_preview=%s",
        len(text),
        num_cards,
        _sanitize_text_for_logging(text, Config.LOG_MAX_TEXT_LEN),
    )
    logger.info("Starting flashcard generation: num_cards=%d", num_cards)
    start_time = time.time()

    _validate_generation_params(text=text, num_cards=num_cards)

    logger.debug(
        "Calling LLM: model=%s, think=%s", Config.OLLAMA_MODEL, Config.SHOULD_THINK
    )
    generation: GenerationResponse = _generate_flashcards_from_messages(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(text, num_cards)},
        ]
    )

    if len(generation.flashcards) > num_cards:
        logger.error(
            "Generated too many flashcards: generated=%d, requested=%d",
            len(generation.flashcards),
            num_cards,
        )
        raise ValueError(
            "Generated too many flashcards (%d) when only %d were requested"
            % (len(generation.flashcards), num_cards)
        )

    elapsed = time.time() - start_time
    logger.info(
        "Flashcard generation completed: generated=%d, requested=%d, duration=%.2fs",
        len(generation.flashcards),
        num_cards,
        elapsed,
    )
    logger.debug("Exiting generate_flashcards: success")

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
    logger.debug(
        "Entering generate_flashcards_from_topic: topic=%s, num_cards=%d",
        topic,
        num_cards,
    )
    logger.info(
        "Starting RAG-based flashcard generation: topic=%s, num_cards=%d",
        topic,
        num_cards,
    )
    start_time = time.time()

    _validate_generation_params(text=topic, num_cards=num_cards)

    logger.debug(
        "Querying VectorForge: url=%s, topic=%s, top_k=%d",
        Config.VECTORFORGE_BASE_URL,
        topic,
        Config.RAG_TOP_K,
    )
    rag_start = time.time()

    response = requests.post(
        url="%s/collections/flashforge/search" % Config.VECTORFORGE_BASE_URL,
        params={"query": topic, "top_k": Config.RAG_TOP_K},
        timeout=Config.TIMEOUT,
    )

    if response.status_code != 200:
        logger.error(
            "VectorForge search failed: status=%d, response=%s",
            response.status_code,
            response.text[:200],
        )
        error = HTTPError(
            "VectorForge search failed with status %d: %s"
            % (response.status_code, response.text)
        )
        error.response = response
        raise error
    if not response.content:
        logger.error("VectorForge returned empty response")
        error = HTTPError("VectorForge returned empty response")
        error.response = response
        raise error

    logger.debug("VectorForge query completed in %.2fs", time.time() - rag_start)

    data = response.json()
    results: list[dict[str, Any]] = data.get("results", [])

    logger.debug("Retrieved %d results from VectorForge", len(results))

    if not results:
        logger.error("No context found for topic: %s", topic)
        raise ValueError("No context found for topic: %s" % topic)

    context_chunks: list[str] = []
    for result in results:
        if "content" in result and result["content"]:
            content = result["content"]
            if isinstance(content, str):
                context_chunks.append(content)

    if not context_chunks:
        logger.error("No valid content retrieved for topic: %s", topic)
        raise ValueError("No valid content retrieved for topic: %s" % topic)

    context = "\n\n".join(context_chunks)

    if len(context) > Config.CONTEXT_MAX_LEN:
        context = context[: Config.CONTEXT_MAX_LEN] + "..."

    logger.debug(
        "Assembled context: chunks=%d, total_len=%d", len(context_chunks), len(context)
    )

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
        logger.error("Failed to generate any flashcards for topic: %s", topic)
        raise ValueError("Failed to generate any flashcards")

    total_elapsed = time.time() - start_time
    logger.info(
        "RAG flashcard generation completed: topic=%s, generated=%d, duration=%.2fs",
        topic,
        len(generation.flashcards),
        total_elapsed,
    )
    logger.debug("Exiting generate_flashcards_from_topic: success")

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
    logger.debug(
        "Entering save_flashcards: num_cards=%d, file_name=%s",
        len(flashcards),
        file_name,
    )
    logger.info("Saving %d flashcards to file: %s", len(flashcards), file_name)

    if len(flashcards) == 0:
        logger.error("Cannot save: flashcards dict is empty")
        raise ValueError("0 flascards were provided - nothing to save")
    if len(file_name) == 0:
        logger.error("Cannot save: file_name is empty")
        raise ValueError("file_name cannot be empty")
    if len(file_name) > Config.MAX_FILE_NAME_LEN:
        logger.error(
            "file_name too long: %d chars (max: %d)",
            len(file_name),
            Config.MAX_FILE_NAME_LEN,
        )
        raise ValueError("file_name too long (%d)" % len(file_name))

    file_path: Path = _validate_safe_path(
        base_dir=Path(Config.OUTPUT_DIR), user_path=file_name
    )

    logger.debug("Validated output path: %s", file_path)

    try:
        with open(file_path, "w") as f:
            json.dump(flashcards, f, indent=2)
    except OSError as e:
        logger.error(
            "Failed to write flashcards to %s: %s", file_path, e.strerror, exc_info=True
        )
        raise OSError(
            "Failed to write flashcards to %s: %s" % (file_path, e.strerror)
        ) from e

    logger.info(
        "Successfully saved flashcards: path=%s, count=%d", file_path, len(flashcards)
    )
    logger.debug("Exiting save_flashcards: success")

    return build_success_response(
        {"message": "Flashcards successfully saved to: %s" % file_path}
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

    logger.debug(
        "Entering export_flashcards_csv: input=%s, output=%s", input_path, output_path
    )
    logger.info("Exporting flashcards to CSV: %s -> %s", in_path, out_path)

    try:
        with open(in_path, "r") as f:
            data: dict[str, str] = json.load(f)
    except FileNotFoundError as e:
        logger.error("JSON file not found: %s", in_path, exc_info=True)
        raise FileNotFoundError(
            "JSON File not found at location: '%s'" % in_path
        ) from e
    except OSError as e:
        logger.error(
            "Failed to read JSON file %s: %s", in_path, e.strerror, exc_info=True
        )
        raise OSError(
            "Failed to read flashcards from %s: %s" % (in_path, e.strerror)
        ) from e

    num_cards = len(data.get("flashcards", []))
    logger.debug("Loaded %d flashcards from JSON", num_cards)

    df: pd.DataFrame = pd.DataFrame(data.get("flashcards", []))
    df.to_csv(out_path, index=False)

    logger.info("Successfully exported %d flashcards to CSV: %s", num_cards, out_path)
    logger.debug("Exiting export_flashcards_csv: success")

    return build_success_response(
        {"message": "Flashcards successfully converted to CSV: %s" % out_path}
    )

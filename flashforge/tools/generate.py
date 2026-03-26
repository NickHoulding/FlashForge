"""Tools for flashcard generation."""

import json
import logging
import time
from typing import Any

import requests
from requests import HTTPError, Timeout

from ..config import Config
from ..errors import handle_tool_errors
from ..instance import mcp
from ..logging_config import _sanitize_text_for_logging
from ..models import GenerationResponse
from ..prompts import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_RAG,
    build_user_prompt,
    build_user_prompt_rag,
)
from ..utils import (
    _generate_flashcards_from_messages,
    _validate_generation_params,
    build_success_response,
)

logger = logging.getLogger(__name__)


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

    result: dict[str, Any] = generation.model_dump()
    return build_success_response(result)


@mcp.tool(description="Generate flashcards from a topic name using AI research")
@handle_tool_errors
def generate_flashcards_from_topic(topic: str, num_cards: int) -> dict[str, Any]:
    """Generate flashcards by having the LLM research a topic autonomously.

    Args:
        topic: Subject or topic name to generate flashcards about.
        num_cards: Number of flashcards to generate (1 to MAX_CARDS).

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
    try:
        response = requests.post(
            url="%s/collections/vectorforge/search" % Config.VECTORFORGE_BASE_URL,
            json={"query": topic, "top_k": Config.RAG_TOP_K},
            timeout=Config.HTTP_TIMEOUT,
        )
        response.raise_for_status()
    except Timeout:
        raise ValueError(
            "VectorForge request timed out after %d seconds", Config.HTTP_TIMEOUT
        )
    except ConnectionError:
        raise ValueError("Cannot connect to VectorForge - service unavailable")

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

    try:
        data: dict[str, Any] = response.json()
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON from VectorForge")
        raise ValueError("Vectorforge returned invalid JSON: %s", response)

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

    result = generation.model_dump()
    return build_success_response(result)

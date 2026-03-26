"""Tools for saving and exporting flashcard decks."""

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

from ..config import Config
from ..errors import handle_tool_errors
from ..instance import mcp
from ..models import Flashcard
from ..utils import _validate_safe_path, build_success_response

logger = logging.getLogger(__name__)


@mcp.tool(description="Save flashcards to persistent storage")
@handle_tool_errors
def save_flashcards(flashcards: list[Flashcard], deck_name: str) -> dict[str, Any]:
    """Save flashcards to a JSON file in the configured output directory.

    Args:
        flashcards: Dictionary mapping flashcard IDs to their data.
        deck_name: Name of the output file (without directory path).

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
        deck_name,
    )
    logger.info("Saving %d flashcards to file: %s", len(flashcards), deck_name)

    if len(flashcards) == 0:
        logger.error("Cannot save: flashcards dict is empty")
        raise ValueError("0 flashcards were provided - nothing to save")
    if len(deck_name) == 0:
        logger.error("Cannot save: file_name is empty")
        raise ValueError("file_name cannot be empty")
    if len(deck_name) > Config.MAX_FILE_NAME_LEN:
        logger.error(
            "file_name too long: %d chars (max: %d)",
            len(deck_name),
            Config.MAX_FILE_NAME_LEN,
        )
        raise ValueError("file_name too long (%d)" % len(deck_name))

    if not deck_name.endswith(".json"):
        deck_name = deck_name + ".json"

    file_path: Path = _validate_safe_path(
        base_dir=Path(Config.OUTPUT_DIR), user_path=deck_name
    )

    logger.debug("Validated output path: %s", file_path)

    try:
        with open(file_path, "w") as f:
            json.dump(
                {"flashcards": [card.model_dump() for card in flashcards]}, f, indent=2
            )
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
def export_flashcards_csv(deck_name: str) -> dict[str, Any]:
    """Export flashcards from a JSON file to CSV format.

    Reads a JSON file containing flashcards and converts it to a CSV file
    with columns for each flashcard field (question, answer, etc.).

    Args:
        deck_name: Name of the deck file (with or without .json extension)

    Returns:
        Success response dict with confirmation message.

    Raises:
        FileNotFoundError: If input_path does not exist.
        OSError: If input file cannot be read, or if the output file cannot be written.
    """
    if not deck_name.endswith(".json"):
        deck_name += ".json"

    input_path: Path = _validate_safe_path(
        base_dir=Path(Config.OUTPUT_DIR), user_path=deck_name
    )

    logger.debug("Entering export_flashcards_csv: path=%s", input_path)
    logger.info("Exporting flashcards to CSV: deck_name=%s", deck_name)

    try:
        with open(input_path, "r") as f:
            data: dict[str, Any] = json.load(f)
    except json.JSONDecodeError as e:
        logger.error("VectorForge tried to load invalid JSON")
        raise ValueError("Vectorforge tried to load invalid JSON from %s", input_path)
    except FileNotFoundError as e:
        logger.error("JSON file not found: %s", input_path, exc_info=True)

        raise FileNotFoundError(
            "JSON File not found at location: '%s'" % input_path
        ) from e
    except OSError as e:
        logger.error(
            "Failed to read JSON file %s: %s", input_path, e.strerror, exc_info=True
        )
        raise OSError(
            "Failed to read flashcards from %s: %s" % (input_path, e.strerror)
        ) from e

    if "flashcards" not in data:
        raise ValueError("JSON file must contain 'flashcards' key")
    if not isinstance(data["flashcards"], list):
        raise ValueError("'flashcards' must be a list")

    num_cards = len(data["flashcards"])
    logger.debug("Loaded %d flashcards from JSON", num_cards)

    flashcards: list[dict[str, str]] = data["flashcards"]
    df: pd.DataFrame = pd.DataFrame(flashcards)
    output_path: Path = input_path.with_suffix(".csv")
    df.to_csv(output_path, index=False)

    logger.info(
        "Successfully exported %d flashcards to CSV: %s", num_cards, output_path
    )
    logger.debug("Exiting export_flashcards_csv: success")

    return build_success_response(
        {"message": "Flashcards successfully converted to CSV: %s" % output_path}
    )

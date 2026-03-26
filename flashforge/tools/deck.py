"""Flashcard deck management tools for listing, retrieving, and deleting decks."""

import json
import logging
import os
from pathlib import Path
from typing import Any

from ..config import Config
from ..errors import handle_tool_errors
from ..instance import mcp
from ..utils import _validate_safe_path, build_success_response

logger = logging.getLogger(__name__)


@mcp.tool(description="List all available flashcard decks")
@handle_tool_errors
def list_decks() -> dict[str, Any]:
    """List all available flashcard decks in the output directory.

    Returns:
      Dictionary with success status and list of deck file paths.

    Raises:
      OSError: If the output directory cannot be read.
    """
    logger.debug("Entering list_decks: output_dir=%s", Config.OUTPUT_DIR)

    try:
        decks: list[Path] = list(Path(Config.OUTPUT_DIR).iterdir())
        json_files: list[str] = [
            os.path.basename(deck) for deck in decks if deck.suffix == ".json"
        ]

        logger.info("Listed %d deck(s) from %s", len(json_files), Config.OUTPUT_DIR)
        logger.debug("Exiting list_decks: found=%d decks", len(json_files))

        return build_success_response({"decks": sorted(json_files)})
    except OSError as e:
        logger.error(
            "Failed to list decks from %s: %s",
            Config.OUTPUT_DIR,
            e.strerror,
            exc_info=True,
        )
        raise


@mcp.tool(description="Retrieve flashcards from a specific deck")
@handle_tool_errors
def get_flashcards(deck_name: str) -> dict[str, Any]:
    """Retrieve all flashcards from a specified deck.

    Args:
      deck_name: Name of the deck file (with or without .json extension).

    Returns:
      Dictionary with success status and flashcard data.

    Raises:
      OSError: If the deck file cannot be read.
      ValueError: If the deck path is invalid or unsafe.
    """
    logger.debug("Entering get_flashcards: deck_name=%s", deck_name)

    if not deck_name.endswith(".json"):
        deck_name += ".json"

    file_path: Path = _validate_safe_path(
        base_dir=Path(Config.OUTPUT_DIR), user_path=deck_name
    )

    logger.info("Reading flashcards from deck: %s", file_path.name)

    try:
        with open(file_path, "r") as f:
            flashcards: dict[str, Any] = json.load(f)

        logger.info(
            "Successfully read %d flashcard(s) from %s",
            len(flashcards.get("flashcards", [])),
            file_path.name,
        )
        logger.debug(
            "Exiting get_flashcards: flashcard_count=%d",
            len(flashcards.get("flashcards", [])),
        )

        return build_success_response(flashcards)
    except OSError as e:
        logger.error(
            "Failed to read flashcards from %s: %s",
            file_path,
            e.strerror,
            exc_info=True,
        )
        raise OSError(
            "Failed to read flashcards from %s: %s" % (file_path, e.strerror)
        ) from e


@mcp.tool(description="Delete a flashcard deck by name")
@handle_tool_errors
def delete_deck(deck_name: str) -> dict[str, Any]:
    """Delete a flashcard deck from the output directory.

    Args:
      deck_name: Name of the deck file to delete (with or without .json extension).

    Returns:
      Dictionary with success status and confirmation message.

    Raises:
      FileNotFoundError: If the specified deck does not exist.
      ValueError: If the deck path is invalid or unsafe.
    """
    logger.debug("Entering delete_deck: deck_name=%s", deck_name)

    if not deck_name.endswith(".json"):
        deck_name += ".json"

    file_path: Path = _validate_safe_path(
        base_dir=Path(Config.OUTPUT_DIR), user_path=deck_name
    )

    logger.info("Deleting deck: %s", file_path.name)

    try:
        os.remove(Path(file_path))

        logger.info("Successfully deleted deck: %s", deck_name)
        logger.debug("Exiting delete_deck: deleted=%s", file_path.name)

        return build_success_response(
            {"message": f"Deck: '{deck_name}' successfully deleted."}
        )
    except FileNotFoundError as e:
        logger.error("JSON file not found: %s", file_path, exc_info=True)

        raise FileNotFoundError(
            "JSON File not found at location: '%s'" % file_path
        ) from e

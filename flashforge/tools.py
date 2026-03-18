"""All tools for the FlashForge MCP server."""

import json
import os
from typing import Any

import pandas as pd
from fastmcp import tools

from .instance import mcp

# =============================================================================
# Generation Tools
# =============================================================================


@mcp.tool
def generate_flashcards(text: str) -> dict[str, Any]:
    """"""
    raise NotImplementedError


@mcp.tool
def generate_flashcards_from_topic(topic: str) -> dict[str, Any]:
    """"""
    raise NotImplementedError


# =============================================================================
# Persistance Tools
# =============================================================================


@mcp.tool
def save_flashcards(flashcards: dict[str, str]) -> dict[str, Any]:
    """"""
    raise NotImplementedError


@mcp.tool
def export_flashcards_csv(file_path: str) -> dict[str, Any]:
    """"""
    raise NotImplementedError

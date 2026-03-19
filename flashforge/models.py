"""Pydantic models for flashcard generation and validation.

Contains Flashcard and GenerationResponse models used by the MCP tools.
"""

from pydantic import BaseModel, Field

from .config import Config


class Flashcard(BaseModel):
    """A single flashcard with a question and answer pair.

    Represents one study flashcard generated from source material, with
    configurable maximum lengths for both question and answer fields.
    """

    question: str = Field(
        ...,
        description="This flashcard's question",
        min_length=1,
        max_length=Config.QUESTION_MAX_LEN,
    )
    answer: str = Field(
        ...,
        description="The answer to this flashcard's question",
        min_length=1,
        max_length=Config.ANSWER_MAX_LEN,
    )


class GenerationResponse(BaseModel):
    """Response wrapper for flashcard generation operations.

    Contains a list of generated flashcards returned by the AI model.
    """

    flashcards: list[Flashcard] = Field(..., description="A list of Flashcards")

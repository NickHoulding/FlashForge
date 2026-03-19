"""Prompt templates for flashcard generation.

Contains system prompts and user prompt builders for both text-based
and RAG-based flashcard generation workflows.
"""

# =============================================================================
# Text-Based Generation Prompts
# =============================================================================

SYSTEM_PROMPT = (
    "You are an expert at creating effective study flashcards. "
    "Generate flashcards that:\n"
    "- Ask clear, specific questions with unambiguous answers\n"
    "- Focus on one concept per card\n"
    "- Avoid yes/no questions; prefer 'what', 'how', 'why'\n"
    "- Use concise language without unnecessary elaboration\n"
    "- Include enough context in the question to be self-contained"
)


def build_user_prompt(text: str, num_cards: int) -> str:
    """Build the user prompt for text-based flashcard generation.

    Args:
        text: Source material to generate flashcards from.
        num_cards: Number of flashcards to generate.

    Returns:
        Formatted user prompt string with text and card count.
    """
    return (
        f"Generate exactly {num_cards} flashcards from the following text. "
        "Extract the most important concepts and facts.\n\n"
        f"{text}"
    )


# =============================================================================
# RAG-Based Generation Prompts
# =============================================================================

SYSTEM_PROMPT_RAG = (
    "You are an expert at creating effective study flashcards from retrieved context. "
    "Generate flashcards that:\n"
    "- Are based ONLY on the provided context documents\n"
    "- Ask clear, specific questions with unambiguous answers\n"
    "- Focus on one concept per card\n"
    "- Avoid yes/no questions; prefer 'what', 'how', 'why'\n"
    "- Use concise language without unnecessary elaboration\n"
    "- Include enough context in the question to be self-contained\n"
    "- Do NOT make up information beyond what's in the context\n"
    "- If context is insufficient, generate fewer cards rather than inventing facts"
)


def build_user_prompt_rag(topic: str, context: str, num_cards: int) -> str:
    """Build the user prompt for RAG-based flashcard generation.

    Args:
        topic: The topic the user requested flashcards about.
        context: Retrieved context from the RAG system (concatenated documents).
        num_cards: Target number of flashcards to generate.

    Returns:
        Formatted user prompt with topic, context, and card count.
    """
    return (
        f"Generate up to {num_cards} flashcards about the topic: {topic}\n\n"
        "Base your flashcards ONLY on the following context retrieved from the knowledge base. "
        "Extract the most important and relevant concepts.\n\n"
        "--- CONTEXT ---\n"
        f"{context}\n"
        "--- END CONTEXT ---\n\n"
        f"Generate flashcards focusing on key facts and concepts related to: {topic}"
    )

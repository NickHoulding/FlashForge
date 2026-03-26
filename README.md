# FlashForge ![Python](https://img.shields.io/badge/python-3.11+-blue.svg) ![MCP](https://img.shields.io/badge/MCP-server-green.svg)

> An AI-powered flashcard generation server using Model Context Protocol, Ollama, and VectorForge RAG

## Table of Contents
- [Problem Statement](#problem-statement)
- [What is FlashForge?](#what-is-flashforge)
- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [How to Run](#how-to-run)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Development](#development)

---

## Problem Statement

During my undergraduate studies, I noticed myself wanting an easy and quick way to study course material, but I would always get burnt out after creating comprehensive study flashcard sets manually myself. I realized that AI would be a perfect application for this, as it would take out all the busy work leading to burnout before I even start studying at all. This project aims to bring that vision to life through an MCP server, compatible with Claude Desktop, and able to be set up within just a few minutes.

FlashForge automates the flashcard creation process using AI, transforming raw text or topic queries into high-quality flashcards optimized for spaced repetition learning systems like Quizlet and other study platforms.

---

## What is FlashForge?

FlashForge is a Python-based Model Context Protocol (MCP) server that generates study flashcards using AI. It integrates with Claude Desktop and other MCP clients to provide on-demand flashcard generation from either direct text input or topic-based research using a VectorForge RAG backend.

**FlashForge demonstrates agentic workflows**, where Claude acts as an **orchestrator model** through tool calling, delegating the actual flashcard generation to local Ollama models. This architecture showcases how AI assistants can coordinate multiple AI systems to accomplish complex tasks efficiently.

The server exposes MCP tools that AI assistants can call to:
- Generate flashcards from provided text passages
- Research topics autonomously using a vector database and create flashcards from retrieved context
- Save flashcards to persistent JSON storage
- Export flashcards to CSV format for import into spaced repetition systems
- List, retrieve, and delete saved flashcard decks

FlashForge is designed for students, educators, and lifelong learners who want to automate the creation of effective study materials while maintaining control over content quality through AI-powered generation.

---

## Tech Stack

### **Backend**
- **Python 3.11+**: Core runtime environment
- **FastMCP**: Model Context Protocol server framework
- **Ollama**: Local LLM inference for flashcard generation
- **Requests**: HTTP client for VectorForge RAG integration
- **Pydantic**: Data validation and schema definitions

### **Data & Storage**
- **Pandas**: CSV export functionality
- **JSON**: Primary flashcard storage format
- **VectorForge**: External RAG service for knowledge retrieval (optional)

### **Development Tools**
- **Black**: Code formatting
- **isort**: Import organization
- **mypy**: Static type checking with strict mode
- **pre-commit**: Git hooks for code quality
- **python-json-logger**: Structured logging

### **AI Models**
- Ollama-compatible models
- Configurable model selection via environment variables
- Support for extended reasoning modes

---

## Key Features

### **Flashcard Generation**
- **Text-based generation**: Create flashcards from any text passage
- **Topic-based generation**: Research topics using RAG and generate contextually accurate flashcards
- **Configurable constraints**: Control question/answer length, card count, and text limits
- **Quality control**: Built-in validation to ensure flashcards meet pedagogical best practices

### **Storage & Export**
- **JSON persistence**: Save flashcards to structured JSON files
- **CSV export**: Convert flashcards to CSV format for import into Quizlet and other spaced repetition systems
- **Deck management**: List all saved decks, retrieve flashcards from specific decks, and delete unwanted decks

### **Production-Ready Infrastructure**
- **Structured logging**: JSON logs with rotation for production monitoring
- **Configuration validation**: Comprehensive startup validation of all settings
- **Error handling**: Detailed error messages and logging for troubleshooting
- **Health checks**: Built-in health check endpoint for monitoring

### **MCP Integration**
- **Claude Desktop compatible**: Works seamlessly with Claude as an MCP server
- **Tool-based interface**: Exposes flashcard generation and management as callable tools
- **Configurable timeouts**: Adjustable timeouts for LLM and HTTP requests

---

## Architecture

FlashForge follows a modular architecture designed for maintainability and extensibility:

```
flashforge/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point for running as module
├── config.py            # Centralized configuration with environment variable support
├── errors.py            # Error handling decorators and utilities
├── instance.py          # MCP server instance initialization
├── logging_config.py    # Production-grade structured logging setup
├── models.py            # Pydantic models for flashcards and responses
├── prompts.py           # LLM prompt templates for generation
├── tools/               # MCP tool implementations
│   ├── __init__.py      # Tool registration
│   ├── deck.py          # Deck management tools (list, get, delete)
│   ├── generate.py      # Flashcard generation tools
│   ├── health.py        # Health check endpoint
│   └── persistence.py   # Save and export tools
└── utils.py             # Helper functions for validation and generation
```

### Data Flow

1. **Text-based generation**:
   - User provides text and card count via MCP tool call
   - Text is validated against configured constraints
   - System prompt and user prompt are constructed
   - Ollama generates flashcards using configured model
   - Response is validated and returned to user

2. **Topic-based generation (RAG)**:
   - User provides topic name and card count
   - VectorForge is queried for relevant context
   - Retrieved documents are concatenated and truncated to context limit
   - LLM generates flashcards based only on retrieved context
   - Response is validated and returned to user

3. **Persistence**:
   - User calls save tool with flashcards and filename
   - Path is validated to prevent directory traversal
   - Flashcards are saved to JSON in configured output directory
   - Optional CSV export from JSON available for Quizlet and other study platforms

---

## Getting Started

### Prerequisites

- **Python 3.11 or higher**: Required for type hints and performance features
- **Ollama**: Local LLM server for flashcard generation
  - Pull a model: `ollama pull llama3.1:8b`
- **VectorForge** (optional): Only required for topic-based generation (See [VectorForge documentation](https://github.com/NickHoulding/vectorforge) for setup)
- **uv** (recommended): Fast Python package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/NickHoulding/flashforge.git
cd flashforge

# Create output directory for flashcards
mkdir -p output

# Install dependencies using uv (recommended)
uv sync

# Or install with pip
pip install -e .

# Set up environment variables
cp .env.example .env

# Then, edit .env with your preferred settings
```

### How to Run

**As an MCP server (recommended):**

Add FlashForge to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "flashforge": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/flashforge",
        "flashforge"
      ]
    }
  }
}
```

Restart Claude Desktop, and FlashForge tools will be available in your conversations.

**As a standalone script:**

```bash
uv run flashforge
```

The server runs on stdio transport and will wait for MCP tool calls.

### Environment Variables

FlashForge is highly configurable through environment variables. Copy `.env.example` to `.env` and customize:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| **Ollama Configuration** |
| `FLASHCARD_MODEL` | Ollama model name for generation | `llama3.1:8b` | No |
| `SHOULD_THINK` | Enable extended reasoning mode | `false` | No |
| `OLLAMA_TIMEOUT` | Max seconds for Ollama API responses | `300` | No |
| **VectorForge Configuration** |
| `VECTORFORGE_BASE_URL` | Base URL for VectorForge service | `http://localhost:8000` | No |
| `RAG_TOP_K` | Number of results to retrieve (1-50) | `5` | No |
| `CONTEXT_MAX_LEN` | Max context length (1-50000) | `10000` | No |
| `HTTP_TIMEOUT` | HTTP request timeout in seconds | `30` | No |
| **Flashcard Constraints** |
| `QUESTION_MAX_LEN` | Max question length (1-1000) | `200` | No |
| `ANSWER_MAX_LEN` | Max answer length (1-2000) | `500` | No |
| `MAX_CARDS` | Max cards per request (1-100) | `50` | No |
| `TEXT_MAX_LEN` | Max input text length (1-100000) | `5000` | No |
| **Storage** |
| `OUTPUT_DIR` | Directory for saved flashcards | `./output` | No |
| `MAX_FILE_NAME_LEN` | Max filename length | `255` | No |
| **Logging** |
| `FF_LOG_LEVEL` | Log level (DEBUG/INFO/WARNING/ERROR) | `INFO` | No |
| `FF_LOG_FILE` | Log file path | `.logs/flashforge.log` | No |
| `FF_LOG_JSON_CONSOLE` | Enable JSON console logging | `false` | No |
| `FF_LOG_MAX_TEXT_LEN` | Max text length in logs | `100` | No |
| `FF_LOG_MAX_BYTES` | Max log file size before rotation | `10485760` | No |
| `FF_LOG_BACKUP_COUNT` | Number of backup log files (0-100) | `5` | No |

**Setup instructions:**

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your preferred editor
nvim .env
```

See `.env.example` for detailed descriptions and value ranges for each variable.

---

## Usage

FlashForge is designed to be used through an MCP client like Claude Desktop. Here are examples of typical interactions:

### Basic Flashcard Generation

```python
# In Claude Desktop or any MCP client:
# "Generate 5 flashcards from this text: [paste your study material]"

# Behind the scenes, Claude calls:
generate_flashcards(
    text="Photosynthesis is the process by which plants convert light energy...",
    num_cards=5
)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "flashcards": [
      {
        "question": "What is photosynthesis?",
        "answer": "The process by which plants convert light energy into chemical energy"
      },
      {
        "question": "What are the two main stages of photosynthesis?",
        "answer": "Light-dependent reactions and the Calvin cycle"
      }
      // ... 3 more flashcards
    ]
  }
}
```

### Topic-Based Generation with RAG

```python
# In Claude Desktop:
# "Research mitochondria and create 10 flashcards"

# Claude calls:
generate_flashcards_from_topic(
    topic="mitochondria",
    num_cards=10
)
```

This queries your VectorForge knowledge base, retrieves relevant context, and generates flashcards based only on the retrieved information.

### Saving Flashcards

```python
# In Claude Desktop:
# "Save these flashcards as biology_chapter_3"

# Claude calls:
save_flashcards(
    flashcards=[
        {"question": "What is photosynthesis?", "answer": "..."},
        {"question": "What are chloroplasts?", "answer": "..."}
    ],
    deck_name="biology_chapter_3"
)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Flashcards successfully saved to: /path/to/output/biology_chapter_3.json"
  }
}
```

### Exporting to CSV

```python
# In Claude Desktop:
# "Export biology_chapter_3 to CSV for Quizlet import"

# Claude calls:
export_flashcards_csv(deck_name="biology_chapter_3")
```

The CSV file will have columns for `question` and `answer` that can be imported directly into Quizlet, Knowt, Anki, or other spaced repetition systems.

### Listing Available Decks

```python
# In Claude Desktop:
# "What flashcard decks do I have saved?"

# Claude calls:
list_decks()
```

**Response:**
```json
{
  "success": true,
  "data": {
    "decks": [
      "biology_chapter_3.json",
      "chemistry_midterm.json",
      "history_wwii.json"
    ]
  }
}
```

### Retrieving Flashcards from a Deck

```python
# In Claude Desktop:
# "Show me the flashcards from biology_chapter_3"

# Claude calls:
get_flashcards(deck_name="biology_chapter_3")
```

**Response:**
```json
{
  "success": true,
  "data": {
    "flashcards": [
      {
        "question": "What is photosynthesis?",
        "answer": "The process by which plants convert light energy into chemical energy"
      },
      {
        "question": "What are the two main stages of photosynthesis?",
        "answer": "Light-dependent reactions and the Calvin cycle"
      }
    ]
  }
}
```

### Deleting a Deck

```python
# In Claude Desktop:
# "Delete the old_notes.json deck"

# Claude calls:
delete_deck(deck_name="old_notes")
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Deck: 'old_notes.json' successfully deleted."
  }
}
```

### Health Check

```python
# Verify server is running:
health_check()
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy"
  }
}
```

---

## API Reference

FlashForge exposes the following MCP tools:

### `generate_flashcards(text: str, num_cards: int)`

Generate flashcards from provided text using AI.

**Parameters:**
- `text` (str): Source material to extract flashcard Q&A pairs from
- `num_cards` (int): Number of flashcards to generate (1 to MAX_CARDS)

**Returns:**
- `dict[str, Any]`: Success response containing list of flashcards with `question` and `answer` fields

**Raises:**
- `ValueError`: If text is empty, exceeds TEXT_MAX_LEN, num_cards is invalid, or generation produces invalid output

**Example:**
```python
result = generate_flashcards(
    text="The mitochondria is the powerhouse of the cell...",
    num_cards=3
)
```

---

### `generate_flashcards_from_topic(topic: str, num_cards: int)`

Generate flashcards by researching a topic using VectorForge RAG.

**Parameters:**
- `topic` (str): Subject or topic name to generate flashcards about
- `num_cards` (int): Number of flashcards to generate (1 to MAX_CARDS)

**Returns:**
- `dict[str, Any]`: Success response containing generated flashcards

**Raises:**
- `ValueError`: If topic is empty, num_cards is invalid, or no context found
- `HTTPError`: If VectorForge request fails
- `ConnectionError`: If VectorForge service is unavailable
- `Timeout`: If VectorForge request exceeds HTTP_TIMEOUT

**Example:**
```python
result = generate_flashcards_from_topic(
    topic="cellular respiration",
    num_cards=10
)
```

---

### `save_flashcards(flashcards: list[Flashcard], deck_name: str)`

Save flashcards to persistent JSON storage.

**Parameters:**
- `flashcards` (list[Flashcard]): List of flashcard objects to save
- `deck_name` (str): Name of the deck (without directory path or extension)

**Returns:**
- `dict[str, Any]`: Success response with confirmation message and save location

**Raises:**
- `ValueError`: If flashcards list is empty, deck_name is empty/invalid, or exceeds MAX_FILE_NAME_LEN
- `OSError`: If file cannot be created or written

**Example:**
```python
result = save_flashcards(
    flashcards=[
        {"question": "What is photosynthesis?", "answer": "..."},
        {"question": "What are chloroplasts?", "answer": "..."}
    ],
    deck_name="biology_chapter_3"
)
```

---

### `export_flashcards_csv(deck_name: str)`

Export flashcards from JSON to CSV format.

**Parameters:**
- `deck_name` (str): Name of the deck file (with or without .json extension)

**Returns:**
- `dict[str, Any]`: Success response with confirmation message

**Raises:**
- `FileNotFoundError`: If deck_name does not exist
- `OSError`: If input file cannot be read or output file cannot be written
- `ValueError`: If JSON is invalid or missing required keys

**Example:**
```python
result = export_flashcards_csv(deck_name="biology_chapter_3")
# Creates biology_chapter_3.csv in the same directory
```

---

### `list_decks()`

List all available flashcard decks in the output directory.

**Returns:**
- `dict[str, Any]`: Success response containing a list of deck filenames

**Raises:**
- `OSError`: If the output directory cannot be read

**Example:**
```python
result = list_decks()
# {"success": true, "data": {"decks": ["biology.json", "chemistry.json"]}}
```

---

### `get_flashcards(deck_name: str)`

Retrieve all flashcards from a specific deck.

**Parameters:**
- `deck_name` (str): Name of the deck file (with or without .json extension)

**Returns:**
- `dict[str, Any]`: Success response containing flashcard data

**Raises:**
- `OSError`: If the deck file cannot be read
- `ValueError`: If the deck path is invalid or unsafe

**Example:**
```python
result = get_flashcards(deck_name="biology_chapter_3")
# Returns all flashcards from biology_chapter_3.json
```

---

### `delete_deck(deck_name: str)`

Delete a flashcard deck from the output directory.

**Parameters:**
- `deck_name` (str): Name of the deck file to delete (with or without .json extension)

**Returns:**
- `dict[str, Any]`: Success response with confirmation message

**Raises:**
- `FileNotFoundError`: If the specified deck does not exist
- `ValueError`: If the deck path is invalid or unsafe

**Example:**
```python
result = delete_deck(deck_name="old_notes")
# {"success": true, "data": {"message": "Deck: 'old_notes.json' successfully deleted."}}
```

---

### `health_check()`

Verify the MCP server is operational.

**Returns:**
- `dict[str, Any]`: Success response with status "healthy"

**Example:**
```python
result = health_check()
# {"success": true, "data": {"status": "healthy"}}
```

---

## Development

### Code Quality

FlashForge uses strict code quality tools:

```bash
# Format code
isort flashforge/
black flashforge/

# Type checking
mypy flashforge/

# Pre-commit hooks (runs all checks)
pre-commit run --all-files
```

### Project Structure

- `flashforge/__init__.py`: Package initialization
- `flashforge/__main__.py`: Entry point for running as module
- `flashforge/config.py`: Configuration management with environment variables
- `flashforge/errors.py`: Error handling utilities
- `flashforge/instance.py`: MCP server instance initialization
- `flashforge/logging_config.py`: Production logging setup with rotation
- `flashforge/models.py`: Pydantic models for validation
- `flashforge/prompts.py`: LLM prompt templates
- `flashforge/tools/`: MCP tool implementations
  - `deck.py`: Deck management tools
  - `generate.py`: Flashcard generation tools
  - `health.py`: Health check endpoint
  - `persistence.py`: Save and export tools
- `flashforge/utils.py`: Helper functions

### Running Tests

```bash
# Run all tests (when test suite is added)
pytest tests/

# Run with coverage
pytest --cov=flashforge tests/
```

---

## License

This project is currently unlicensed. Please contact the repository owner for licensing information.

---

<div align="center">
  <strong>FlashForge</strong>
</div>

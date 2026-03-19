"""Error-handling decorator for FlashForge MCP tool functions."""

import functools
from typing import Any, Callable, cast

from pydantic import ValidationError

from .utils import build_error_response


def handle_tool_errors(
    func: Callable[..., dict[str, Any]],
) -> Callable[..., dict[str, Any]]:
    """Decorator to handle errors from MCP tool invocations.

    Wraps tool functions to catch exceptions and convert them into
    standardized error response dictionaries.

    Args:
        func: The MCP tool function to wrap with error handling.

    Returns:
        Wrapped function that returns error responses instead of raising.
    """

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            return func(*args, **kwargs)

        except ValidationError:
            return build_error_response(
                Exception("Flashcard generation failed"),
                details="Object could not be validated/invalid JSON output",
            )
        except Exception as e:
            return build_error_response(Exception("Operation failed"), details=str(e))

    return sync_wrapper

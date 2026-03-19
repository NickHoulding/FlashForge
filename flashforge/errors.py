"""Error-handling decorator for FlashForge MCP tool functions."""

import functools
from typing import Any, Callable, cast

from pydantic import ValidationError
from requests import HTTPError

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

        except ValidationError as e:
            return build_error_response(
                Exception("Flashcard generation failed"),
                details={
                    "error_type": "validation_error",
                    "message": "llm returned invalid json or schema-incompatible output",
                    "suggestion": "check model output format and schema compatibility",
                    "validation_details": str(e),
                },
            )
        except HTTPError as e:
            status_code = (
                getattr(e.response, "status_code", None)
                if hasattr(e, "response")
                else None
            )
            error_details = {
                "error_type": "http_error",
                "message": "Failed to connect to VectorForge RAG service",
                "http_details": str(e),
            }

            if status_code == 404:
                error_details["suggestion"] = (
                    "Collection 'flashforge' not found. Create it in VectorForge first"
                )
            elif status_code == 503:
                error_details["suggestion"] = (
                    "VectorForge service unavailable. Check if the service is running"
                )
            elif status_code and status_code >= 500:
                error_details["suggestion"] = "VectorForge server error"
            else:
                error_details["suggestion"] = (
                    "Verify VECTORFORGE_BASE_URL is correct and VectorForge is running"
                )

            error_details["status_code"] = str(status_code)

            return build_error_response(
                Exception("VectorForge connection failed"), details=error_details
            )
        except OSError as e:
            return build_error_response(
                Exception(""),
                details={
                    "error_type": "os_error",
                    "message": "FlashForge failed to write flashcard data to JSON file",
                    "suggestion": "Make sure the save path points to an existing directory",
                    "validation_details": str(e),
                },
            )
        except Exception as e:
            return build_error_response(
                Exception("Operation failed"),
                details={
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "suggestion": "Check logs for more details",
                },
            )

    return sync_wrapper

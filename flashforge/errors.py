"""Error-handling decorator for FlashForge MCP tool functions."""

import functools
import logging
from typing import Any, Callable

from pydantic import ValidationError
from requests import HTTPError

from .utils import build_error_response

logger = logging.getLogger(__name__)


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
        """"""
        try:
            return func(*args, **kwargs)

        except ValidationError as e:
            logger.error(
                "Validation error in %s: %s",
                func.__name__,
                str(e),
                exc_info=True,
            )
            return build_error_response(
                error=e,
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
            logger.error(
                "HTTP error in %s: status_code=%s, error=%s",
                func.__name__,
                status_code,
                str(e),
                exc_info=True,
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

            return build_error_response(error=e, details=error_details)
        except FileNotFoundError as e:
            logger.error(
                "File not found error in %s: %s",
                func.__name__,
                str(e),
                exc_info=True,
            )
            return build_error_response(
                error=e,
                details={
                    "error_type": "file_not_found_error",
                    "message": "Input file does not exist",
                    "suggestion": "Verify the input path exists and points to a readable file",
                    "error_details": str(e),
                },
            )
        except OSError as e:
            logger.error(
                "OS error in %s: %s",
                func.__name__,
                str(e),
                exc_info=True,
            )
            return build_error_response(
                error=e,
                details={
                    "error_type": "os_error",
                    "message": "FlashForge could not read or write a file",
                    "suggestion": "Check file permissions, parent directory existence, and available disk space",
                    "error_details": str(e),
                },
            )
        except Exception as e:
            logger.error(
                "Unexpected error in %s: %s (%s)",
                func.__name__,
                str(e),
                type(e).__name__,
                exc_info=True,
            )
            return build_error_response(
                error=e,
                details={
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "suggestion": "Check logs for more details",
                },
            )

    return sync_wrapper

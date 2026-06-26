"""Standardized HTTP JSON response utility for HELIX REST APIs."""

from typing import Any, Dict, Tuple
from flask import jsonify, Response

def make_success_response(data: Any, status_code: int = 200) -> Tuple[Response, int]:
    """Generates a standardized JSON success response.

    Args:
        data: The payload data (dict, list, string, etc.).
        status_code: HTTP status code. Defaults to 200.

    Returns:
        Tuple[Response, int]: Standardized success response tuple.
    """
    response_body: Dict[str, Any] = {
        "success": True,
        "data": data
    }
    return jsonify(response_body), status_code

def make_error_response(message: str, status_code: int = 400) -> Tuple[Response, int]:
    """Generates a standardized JSON error response.

    Args:
        message: Descriptive error message.
        status_code: HTTP status code. Defaults to 400.

    Returns:
        Tuple[Response, int]: Standardized error response tuple.
    """
    response_body: Dict[str, Any] = {
        "success": False,
        "message": message
    }
    return jsonify(response_body), status_code

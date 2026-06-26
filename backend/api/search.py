"""REST API endpoints for performing global search on disaster events."""

import logging
from flask import Blueprint, request, Response
from typing import Tuple
from backend.services.search_service import search_events
from backend.utils.response import make_success_response, make_error_response

logger = logging.getLogger(__name__)

search_bp = Blueprint("search", __name__)

@search_bp.route("/search", methods=["GET"])
def search() -> Tuple[Response, int]:
    """Searches disaster events by query parameter q.

    Returns:
        Tuple[Response, int]: JSON response containing matching events list.
    """
    logger.info("Incoming Request: GET /api/search")
    try:
        q = request.args.get("q")
        if not q or not q.strip():
            logger.warning("Warning Response: GET /api/search with empty query.")
            return make_success_response([])
            
        events = search_events(q.strip())
        logger.info("Request Completed: GET /api/search q='%s' succeeded. Returned %d events.", q.strip(), len(events))
        return make_success_response(events)
    except Exception as err:
        logger.error("Error Response: GET /api/search failed: %s", err)
        return make_error_response("Internal Server Error", 500)

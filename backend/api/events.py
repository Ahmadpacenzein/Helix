"""REST API endpoints for retrieving disaster events and timeline data."""

import logging
from flask import Blueprint, request, Response
from typing import Tuple
from backend.services.event_service import get_events, get_event_detail, get_timeline
from backend.utils.response import make_success_response, make_error_response

logger = logging.getLogger(__name__)

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["GET"])
def list_events() -> Tuple[Response, int]:
    """Retrieves list of disaster events filtered by optional query params.

    Returns:
        Tuple[Response, int]: JSON response containing filtered events list.
    """
    logger.info("Incoming Request: GET /api/events")
    try:
        # Extract query parameters
        country = request.args.get("country")
        category = request.args.get("category")
        status = request.args.get("status")
        date = request.args.get("date")
        
        # Validations (if any are incorrect/invalid, handle appropriately)
        # Note: Empty string parameters should be ignored/treated as None
        country_param = country if country and country.strip() else None
        category_param = category if category and category.strip() else None
        status_param = status if status and status.strip() else None
        date_param = date if date and date.strip() else None
        
        events = get_events(
            country=country_param,
            category=category_param,
            status=status_param,
            date=date_param
        )
        logger.info("Request Completed: GET /api/events succeeded. Returned %d events.", len(events))
        return make_success_response(events)
    except Exception as err:
        logger.error("Error Response: GET /api/events failed: %s", err)
        return make_error_response("Internal Server Error", 500)

@events_bp.route("/events/<event_id>", methods=["GET"])
def event_detail(event_id: str) -> Tuple[Response, int]:
    """Retrieves details of a single disaster event.

    Args:
        event_id: The unique Event ID (e.g. EONET_10793).

    Returns:
        Tuple[Response, int]: JSON response containing event details.
    """
    logger.info("Incoming Request: GET /api/events/%s", event_id)
    try:
        if not event_id or not event_id.strip():
            return make_error_response("Invalid Event ID", 400)
            
        event = get_event_detail(event_id.strip())
        if event is None:
            logger.warning("Error Response: Event ID %s not found.", event_id)
            return make_error_response("Event not found", 404)
            
        logger.info("Request Completed: GET /api/events/%s succeeded.", event_id)
        return make_success_response(event)
    except Exception as err:
        logger.error("Error Response: GET /api/events/%s failed: %s", event_id, err)
        return make_error_response("Internal Server Error", 500)

@events_bp.route("/timeline", methods=["GET"])
def timeline() -> Tuple[Response, int]:
    """Retrieves a timeline of the 20 latest disaster events.

    Returns:
        Tuple[Response, int]: JSON response containing timeline events list.
    """
    logger.info("Incoming Request: GET /api/timeline")
    try:
        events = get_timeline(limit=20)
        logger.info("Request Completed: GET /api/timeline succeeded. Returned %d events.", len(events))
        return make_success_response(events)
    except Exception as err:
        logger.error("Error Response: GET /api/timeline failed: %s", err)
        return make_error_response("Internal Server Error", 500)

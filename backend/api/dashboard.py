"""REST API endpoints for dashboard summaries and sync status."""

import logging
from flask import Blueprint, Response
from typing import Tuple
from backend.services.dashboard_service import get_dashboard_summary, get_sync_status
from backend.utils.response import make_success_response, make_error_response

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard() -> Tuple[Response, int]:
    """Retrieves general dashboard metrics.

    Returns:
        Tuple[Response, int]: JSON response containing dashboard metrics card counts.
    """
    logger.info("Incoming Request: GET /api/dashboard")
    try:
        data = get_dashboard_summary()
        if data is None:
            # If aggregation hasn't run yet, return default empty dict or message
            data = {
                "total_events": 0,
                "active_events": 0,
                "total_categories": 0,
                "total_countries": 0,
                "updated_today": 0,
                "last_sync": None
            }
        logger.info("Request Completed: GET /api/dashboard succeeded.")
        return make_success_response(data)
    except Exception as err:
        logger.error("Error Response: GET /api/dashboard failed: %s", err)
        return make_error_response("Internal Server Error", 500)

@dashboard_bp.route("/sync/status", methods=["GET"])
def sync_status() -> Tuple[Response, int]:
    """Retrieves information about the latest synchronization execution cycle.

    Returns:
        Tuple[Response, int]: JSON response containing sync log status.
    """
    logger.info("Incoming Request: GET /api/sync/status")
    try:
        data = get_sync_status()
        if data is None:
            # Return empty structure as specified by EONET specification v1
            data = {
                "last_sync": None,
                "inserted": 0,
                "updated": 0,
                "duration": "0.00s",
                "status": "No Sync Run"
            }
        logger.info("Request Completed: GET /api/sync/status succeeded.")
        return make_success_response(data)
    except Exception as err:
        logger.error("Error Response: GET /api/sync/status failed: %s", err)
        return make_error_response("Internal Server Error", 500)

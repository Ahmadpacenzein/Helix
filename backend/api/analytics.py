"""REST API endpoints for country and category analytics."""

import logging
from flask import Blueprint, Response
from typing import Tuple
from backend.services.analytics_service import get_country_analytics, get_category_analytics
from backend.utils.response import make_success_response, make_error_response

logger = logging.getLogger(__name__)

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/country", methods=["GET"])
def country_analytics() -> Tuple[Response, int]:
    """Retrieves aggregated statistics grouped by country.

    Returns:
        Tuple[Response, int]: JSON response containing country analytics.
    """
    logger.info("Incoming Request: GET /api/analytics/country")
    try:
        data = get_country_analytics()
        logger.info("Request Completed: GET /api/analytics/country succeeded. Returned %d records.", len(data))
        return make_success_response(data)
    except Exception as err:
        logger.error("Error Response: GET /api/analytics/country failed: %s", err)
        return make_error_response("Internal Server Error", 500)

@analytics_bp.route("/analytics/category", methods=["GET"])
def category_analytics() -> Tuple[Response, int]:
    """Retrieves aggregated statistics grouped by disaster category.

    Returns:
        Tuple[Response, int]: JSON response containing category analytics.
    """
    logger.info("Incoming Request: GET /api/analytics/category")
    try:
        data = get_category_analytics()
        logger.info("Request Completed: GET /api/analytics/category succeeded. Returned %d records.", len(data))
        return make_success_response(data)
    except Exception as err:
        logger.error("Error Response: GET /api/analytics/category failed: %s", err)
        return make_error_response("Internal Server Error", 500)

"""Fetch service for retrieving disaster event data from NASA EONET API.

This service communicates with the NASA Earth Observatory Natural Event Tracker
(EONET) API, validates the HTTP response, and returns the raw JSON response.
It does not perform database persistence or data transformation.
"""

import logging
import time
from typing import Any, Dict
import requests

from config import Config

logger = logging.getLogger(__name__)

def fetch_events(timeout: int = 10) -> Dict[str, Any]:
    """Retrieves disaster event data from the NASA EONET API.

    Performs an HTTP GET request to the configured NASA EONET API URL,
    validates the HTTP status and JSON response structure, and returns the
    raw dictionary containing natural events data.

    Args:
        timeout: The request timeout in seconds. Defaults to 10.

    Returns:
        Dict[str, Any]: The parsed JSON response from the NASA EONET API.

    Raises:
        requests.RequestException: If the HTTP request fails or times out.
        ValueError: If the response is not valid JSON or lacks required fields.
    """
    url = Config.NASA_API_URL
    logger.info("Request Started: Fetching events from NASA EONET API URL: %s", url)
    
    start_time = time.perf_counter()
    try:
        response = requests.get(url, timeout=timeout)
        duration = time.perf_counter() - start_time
        
        logger.info("Request Completed: Status %d, Response Time: %.2fs", response.status_code, duration)
        
        # Raise an HTTPError if the response code was not successful (2xx)
        response.raise_for_status()
        
    except requests.Timeout as err:
        logger.error("Request failed: Timeout after %d seconds contacting NASA API: %s", timeout, err)
        raise
    except requests.ConnectionError as err:
        logger.error("Request failed: Connection error contacting NASA API: %s", err)
        raise
    except requests.HTTPError as err:
        logger.error("Request failed: HTTP error response from NASA API: %s", err)
        raise
    except requests.RequestException as err:
        logger.error("Request failed: General requests exception: %s", err)
        raise

    # Parse and validate JSON response
    try:
        data = response.json()
    except ValueError as err:
        logger.error("Request failed: Failed to parse response JSON: %s", err)
        raise ValueError(f"Invalid JSON response: {err}") from err

    if not data:
        logger.error("Request failed: NASA EONET API returned an empty response.")
        raise ValueError("Empty response received from NASA EONET API")

    # NASA EONET API V3 events list is under "events" key
    events = data.get("events")
    if events is None:
        logger.error("Request failed: 'events' key is missing from NASA EONET API response structure.")
        raise ValueError("Invalid EONET API response format: missing 'events' list")

    logger.info("Success: Retrieved %d disaster events from NASA EONET API.", len(events))
    return data

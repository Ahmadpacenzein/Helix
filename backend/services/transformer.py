"""Data Transformation Service for the HELIX project.

Converts raw NASA EONET event JSON structures into the official HELIX MongoDB
document schema. Validates required fields and normalizes coordinates.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parses an ISO 8601 date string from NASA EONET into a UTC datetime object.

    Args:
        date_str: The ISO date string (e.g., '2026-06-25T18:30:00Z').

    Returns:
        Optional[datetime]: The parsed UTC datetime object, or None if invalid.
    """
    if not date_str:
        return None
    try:
        # Standardize 'Z' to '+00:00' if necessary, though Python 3.11+ supports 'Z'
        if date_str.endswith("Z"):
            date_str = date_str[:-1] + "+00:00"
        return datetime.fromisoformat(date_str)
    except ValueError as err:
        logger.warning("Failed to parse date string '%s': %s", date_str, err)
        return None

def resolve_country(title: str, latitude: float, longitude: float) -> Optional[str]:
    """Resolves country name based on title keywords and coordinates bounding boxes."""
    if not title:
        return None
        
    title_lower = title.lower()
    
    # 1. Keyword mapping in title
    keywords = {
        "united states": "United States",
        " usa": "United States",
        "california": "United States",
        "oregon": "United States",
        "washington": "United States",
        "alaska": "United States",
        "hawaii": "United States",
        "oklahoma": "United States",
        "texas": "United States",
        "canada": "Canada",
        "alberta": "Canada",
        "jasper": "Canada",
        "indonesia": "Indonesia",
        "lewotobi": "Indonesia",
        "sinabung": "Indonesia",
        "merapi": "Indonesia",
        "japan": "Japan",
        "sakurajima": "Japan",
        "kyushu": "Japan",
        "chile": "Chile",
        "valparaiso": "Chile",
        "australia": "Australia",
        "queensland": "Australia",
        "iceland": "Iceland",
        "katla": "Iceland",
        "grindavik": "Iceland",
        "philippines": "Philippines",
        "luzon": "Philippines",
        "ewiniar": "Philippines",
        "china": "China",
        "sichuan": "China",
        "gansu": "China",
        "germany": "Germany",
        "elbe": "Germany",
        "india": "India",
        "assam": "India",
        "remal": "India",
        "italy": "Italy",
        "etna": "Italy",
        "mexico": "Mexico",
        "popocatepetl": "Mexico",
        "russia": "Russia",
        "kamchatka": "Russia",
    }
    
    for kw, country in keywords.items():
        if kw in title_lower:
            return country
            
    # 2. Coordinates bounding boxes fallback
    # Indonesia
    if -11.0 <= latitude <= 6.0 and 95.0 <= longitude <= 141.0:
        return "Indonesia"
    # Japan
    if 24.0 <= latitude <= 46.0 and 123.0 <= longitude <= 146.0:
        return "Japan"
    # United States
    if (24.0 <= latitude <= 50.0 and -125.0 <= longitude <= -67.0) or (19.0 <= latitude <= 22.0 and -160.0 <= longitude <= -154.0) or (51.0 <= latitude <= 72.0 and -179.0 <= longitude <= -130.0):
        return "United States"
    # Canada
    if 41.0 <= latitude <= 84.0 and -141.0 <= longitude <= -52.0:
        return "Canada"
    # Australia
    if -44.0 <= latitude <= -10.0 and 113.0 <= longitude <= 154.0:
        return "Australia"
    # Iceland
    if 63.0 <= latitude <= 67.0 and -25.0 <= longitude <= -13.0:
        return "Iceland"
    # Philippines
    if 4.0 <= latitude <= 21.0 and 116.0 <= longitude <= 127.0:
        return "Philippines"
    # India
    if 6.0 <= latitude <= 36.0 and 68.0 <= longitude <= 98.0:
        return "India"
    # Chile
    if -56.0 <= latitude <= -17.0 and -76.0 <= longitude <= -67.0:
        return "Chile"
    # Germany
    if 47.0 <= latitude <= 55.0 and 5.0 <= longitude <= 16.0:
        return "Germany"
        
    return None

def transform_event(raw_event: Dict[str, Any], sync_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Transforms a raw NASA EONET event dictionary into the HELIX schema format.

    Validates required fields (event_id, title, category). If validation fails,
    logs the event and returns None.

    Args:
        raw_event: The raw event dictionary from the NASA EONET API.
        sync_id: Optional reference ID for the current synchronization run.

    Returns:
        Optional[Dict[str, Any]]: The transformed HELIX event document, or None if invalid.
    """
    event_id = raw_event.get("id")
    title = raw_event.get("title")
    categories = raw_event.get("categories", [])

    logger.info("Document Transformation Started: Event ID: %s", event_id)

    # 1. Validation check for required fields
    if not event_id:
        logger.error("Invalid Document: Missing required field 'id'. Event: %s", raw_event)
        return None
    if not title:
        logger.error("Invalid Document: Missing required field 'title' for Event ID: %s", event_id)
        return None
    if not categories or not isinstance(categories, list) or len(categories) == 0:
        logger.error("Invalid Document: Missing required field 'categories' or category list is empty for Event ID: %s", event_id)
        return None

    # EONET uses first category in list as the primary one
    primary_category = categories[0]
    category_id = primary_category.get("id")
    category_title = primary_category.get("title")

    if not category_id or not category_title:
        logger.error("Invalid Document: Primary category missing 'id' or 'title' for Event ID: %s", event_id)
        return None

    # 2. Extract geometries (EONET v3 uses 'geometry' while v2/tests use 'geometries')
    raw_geometries = raw_event.get("geometry") or raw_event.get("geometries")
    if not raw_geometries or not isinstance(raw_geometries, list):
        logger.error("Invalid Document: Missing or invalid geometry list for Event ID: %s", event_id)
        return None

    # Map geometry history and check for coordinates validity
    geometry_history: List[Dict[str, Any]] = []
    for index, geom in enumerate(raw_geometries):
        coords = geom.get("coordinates", [])
        if not coords or len(coords) < 2:
            logger.warning("Event ID %s: Geometry at index %d has invalid coordinates: %s", event_id, index, coords)
            continue
        
        geometry_history.append({
            "date": geom.get("date"),
            "type": geom.get("type", "Point"),
            "latitude": coords[1],
            "longitude": coords[0]
        })

    if not geometry_history:
        logger.error("Invalid Document: No valid geometries could be parsed for Event ID: %s", event_id)
        return None

    # Determine Latest Geometry (chronologically the last element)
    latest_geom = geometry_history[-1]

    # Resolve Country name
    lat = latest_geom.get("latitude", 0.0)
    lng = latest_geom.get("longitude", 0.0)
    country_name = resolve_country(title, lat, lng)

    # 3. Handle optional fields
    description = raw_event.get("description")
    if description == "":
        description = None

    # Status mapping based on EONET closed status
    # In EONET v3, closed is either null/empty or contains a date when closed.
    closed_date = raw_event.get("closed")
    status = "closed" if closed_date else "open"

    # Map sources
    raw_sources = raw_event.get("sources", [])
    sources = []
    if isinstance(raw_sources, list):
        for src in raw_sources:
            if isinstance(src, dict) and src.get("id"):
                sources.append({
                    "id": src.get("id"),
                    "url": src.get("url")
                })

    # System Timestamps
    now_utc = datetime.now(timezone.utc)

    # Construct the final HELIX schema
    transformed_doc: Dict[str, Any] = {
        "event_id": event_id,
        "title": title,
        "description": description,
        "category": {
            "id": category_id,
            "name": category_title
        },
        "status": status,
        "country": country_name,  # Out of scope for now, reverse geocoding to be implemented later
        "latest_geometry": latest_geom,
        "geometry_history": geometry_history,
        "sources": sources,
        "created_at": now_utc,
        "updated_at": now_utc,
        "sync_id": sync_id
    }

    logger.info("Successful Transformation for Event ID: %s", event_id)
    return transformed_doc

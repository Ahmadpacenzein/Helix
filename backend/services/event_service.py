"""Service layer for retrieving disaster event data from MongoDB."""

from typing import Any, Dict, List, Optional
from backend.database.mongo import MongoConnection

def get_events(
    country: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieves disaster events filtered by query parameters.

    Args:
        country: Optional country name to filter by.
        category: Optional category name or ID to filter by.
        status: Optional status to filter by (e.g. open/closed).
        date: Optional ISO date string (YYYY-MM-DD) to filter by.

    Returns:
        List[Dict[str, Any]]: List of events matching criteria, excluding _id.
    """
    db = MongoConnection.get_db()
    query_filter: Dict[str, Any] = {}

    if country:
        query_filter["country"] = {"$regex": f"^{country}$", "$options": "i"}

    if category:
        query_filter["$or"] = [
            {"category.id": {"$regex": f"^{category}$", "$options": "i"}},
            {"category.name": {"$regex": f"^{category}$", "$options": "i"}}
        ]

    if status:
        query_filter["status"] = status

    if date:
        # Match by prefix YYYY-MM-DD
        query_filter["latest_geometry.date"] = {"$regex": f"^{date}"}

    # Fetch events sorted by date descending (standard map default view)
    cursor = db.events.find(query_filter, {"_id": 0}).sort("latest_geometry.date", -1)
    return list(cursor)

def get_event_detail(event_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single event document by its unique Event ID.

    Args:
        event_id: The unique EONET Event ID.

    Returns:
        Optional[Dict[str, Any]]: The event document if found, otherwise None.
    """
    db = MongoConnection.get_db()
    doc = db.events.find_one({"event_id": event_id}, {"_id": 0})
    return doc

def get_timeline(limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieves the latest disaster events ordered by date.

    Args:
        limit: Max number of events to return. Defaults to 20.

    Returns:
        List[Dict[str, Any]]: List of recent event documents, excluding _id.
    """
    db = MongoConnection.get_db()
    cursor = db.events.find({}, {"_id": 0}).sort("latest_geometry.date", -1).limit(limit)
    return list(cursor)

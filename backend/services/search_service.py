"""Service layer for performing global search on disaster events."""

from typing import Any, Dict, List
from backend.database.mongo import MongoConnection

def search_events(q: str) -> List[Dict[str, Any]]:
    """Searches disaster events matching title, country, or category.

    Args:
        q: The search query string.

    Returns:
        List[Dict[str, Any]]: List of matching event documents, excluding _id.
    """
    if not q or not q.strip():
        return []

    db = MongoConnection.get_db()
    query = q.strip()
    
    # Perform regex match on title, country, or category name
    search_filter = {
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"country": {"$regex": query, "$options": "i"}},
            {"category.name": {"$regex": query, "$options": "i"}}
        ]
    }
    
    cursor = db.events.find(search_filter, {"_id": 0}).sort("latest_geometry.date", -1)
    return list(cursor)

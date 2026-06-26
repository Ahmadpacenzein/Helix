"""Service layer for retrieving aggregated analytics statistics from MongoDB summary collections."""

from typing import Any, Dict, List
from backend.database.mongo import MongoConnection

def get_country_analytics() -> List[Dict[str, Any]]:
    """Retrieves country aggregation summary statistics.

    Returns:
        List[Dict[str, Any]]: List of country summaries sorted by event count descending, excluding _id.
    """
    db = MongoConnection.get_db()
    cursor = db.country_summary.find({}, {"_id": 0}).sort("total_events", -1)
    return list(cursor)

def get_category_analytics() -> List[Dict[str, Any]]:
    """Retrieves category aggregation summary statistics.

    Returns:
        List[Dict[str, Any]]: List of category summaries sorted by event count descending, excluding _id.
    """
    db = MongoConnection.get_db()
    cursor = db.category_summary.find({}, {"_id": 0}).sort("total_events", -1)
    return list(cursor)

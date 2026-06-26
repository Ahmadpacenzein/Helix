"""Service layer for retrieving dashboard statistics and synchronization status."""

from typing import Any, Dict, Optional
from backend.database.mongo import MongoConnection

def get_dashboard_summary() -> Optional[Dict[str, Any]]:
    """Retrieves the latest dashboard summary statistics.

    Returns:
        Optional[Dict[str, Any]]: The dashboard summary metrics, or None if not found.
    """
    db = MongoConnection.get_db()
    # Find the single summary document (excluding MongoDB ObjectId _id)
    doc = db.dashboard_summary.find_one({}, {"_id": 0})
    return doc

def get_sync_status() -> Optional[Dict[str, Any]]:
    """Retrieves the latest synchronization log status details.

    Returns:
        Optional[Dict[str, Any]]: Sync log document details, or None if none exist.
    """
    db = MongoConnection.get_db()
    # Find the latest sync log document sorted by started_at descending
    doc = db.sync_logs.find_one({}, {"_id": 0}, sort=[("started_at", -1)])
    return doc

"""Sync service to coordinate EONET event fetching, transformation, and storage.

Combines the nasa_fetcher, transformer, and mongo connection modules into
a single operational workflow for synchronizing EONET data to MongoDB.
"""

from datetime import datetime, timezone
import logging
import uuid
from typing import Any, Dict
from backend.database.mongo import MongoConnection
from backend.services.nasa_fetcher import fetch_events
from backend.services.transformer import transform_event

logger = logging.getLogger(__name__)

def sync_events() -> Dict[str, Any]:
    """Retrieves EONET data, transforms each event, and upserts them into MongoDB.

    Logs execution history into the 'sync_logs' collection.

    Returns:
        Dict[str, Any]: A dictionary containing sync statistics.
    """
    logger.info("Starting synchronization run...")
    started_at = datetime.now(timezone.utc)
    sync_id = str(uuid.uuid4())
    
    stats = {
        "total_fetched": 0,
        "inserted": 0,
        "updated": 0,
        "failed": 0
    }
    
    try:
        # 1. Fetch raw data
        raw_data = fetch_events()
        raw_events = raw_data.get("events", [])
        stats["total_fetched"] = len(raw_events)
        
        logger.info("Retrieved %d events. Starting transformation and database insertion.", len(raw_events))
        
        # 2. Iterate and process
        for raw_event in raw_events:
            event_id = raw_event.get("id")
            try:
                # Transform raw event
                transformed_doc = transform_event(raw_event, sync_id=sync_id)
                if not transformed_doc:
                    stats["failed"] += 1
                    logger.warning("Event ID %s was rejected by the transformer.", event_id)
                    continue
                
                # Persist to database
                status = MongoConnection.upsert_event(transformed_doc)
                if status == "inserted":
                    stats["inserted"] += 1
                elif status == "updated":
                    stats["updated"] += 1
                    
            except Exception as err:
                stats["failed"] += 1
                logger.error("Failed to process event ID %s: %s", event_id, err)
                
        finished_at = datetime.now(timezone.utc)
        duration_sec = (finished_at - started_at).total_seconds()
        
        # Write success log
        sync_log = {
            "sync_id": sync_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "inserted": stats["inserted"],
            "updated": stats["updated"],
            "failed": stats["failed"],
            "duration": f"{duration_sec:.2f}s",
            "status": "Success"
        }
        
        db = MongoConnection.get_db()
        db.sync_logs.insert_one(sync_log)
        logger.info("Synchronization completed and logged: %s", sync_log)
        
    except Exception as err:
        finished_at = datetime.now(timezone.utc)
        duration_sec = (finished_at - started_at).total_seconds()
        
        # Write failure log
        sync_log = {
            "sync_id": sync_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "inserted": stats["inserted"],
            "updated": stats["updated"],
            "failed": stats["failed"] or 1,  # If it failed before loop, count as 1 failure
            "duration": f"{duration_sec:.2f}s",
            "status": "Failed"
        }
        
        try:
            db = MongoConnection.get_db()
            db.sync_logs.insert_one(sync_log)
        except Exception as log_err:
            logger.error("Failed to write failure sync log: %s", log_err)
            
        logger.error("Synchronization run failed: %s", err)
        raise
        
    return stats


"""Aggregation Service for the HELIX project.

Responsible for executing aggregation pipelines on the 'events' collection
to generate and refresh the summary collections:
- dashboard_summary (dashboard statistics card metrics)
- country_summary (aggregated statistics by country)
- category_summary (aggregated statistics by category)
"""

from datetime import datetime, timezone
import logging
from pymongo.database import Database
from backend.database.mongo import MongoConnection

logger = logging.getLogger(__name__)

def run_aggregation() -> None:
    """Refreshes all summary collections from the current events collection state.

    Executes aggregation pipelines, deletes previous summary data, and stores the
    updated summaries. Handles failures gracefully.
    """
    logger.info("Aggregation Started: Refreshing summary collections...")
    
    try:
        db = MongoConnection.get_db()
        events_count = db.events.count_documents({})
        
        if events_count == 0:
            logger.info("Events collection is empty. Generating default empty summaries.")
            # Clear previous and write default zeros for dashboard
            db.dashboard_summary.delete_many({})
            db.dashboard_summary.insert_one({
                "total_events": 0,
                "active_events": 0,
                "total_categories": 0,
                "total_countries": 0,
                "updated_today": 0,
                "last_sync": None,
                "generated_at": datetime.now(timezone.utc)
            })
            db.country_summary.delete_many({})
            db.category_summary.delete_many({})
            logger.info("Aggregation Completed: Default empty summaries generated successfully.")
            return

        # 1. Generate Dashboard Summary
        logger.info("Generating Dashboard Summary...")
        total_events = events_count
        active_events = db.events.count_documents({"status": "open"})
        total_categories = len(db.events.distinct("category.id"))
        
        # Count non-null countries
        distinct_countries = db.events.distinct("country")
        total_countries = len([c for c in distinct_countries if c is not None])
        
        # Updated today (UTC day boundary)
        now_utc = datetime.now(timezone.utc)
        start_of_today = datetime(now_utc.year, now_utc.month, now_utc.day, tzinfo=timezone.utc)
        updated_today = db.events.count_documents({"updated_at": {"$gte": start_of_today}})
        
        # Last sync from latest updated event
        latest_event = db.events.find_one(sort=[("updated_at", -1)])
        last_sync = latest_event["updated_at"].isoformat() if latest_event and latest_event.get("updated_at") else None
        
        dashboard_doc = {
            "total_events": total_events,
            "active_events": active_events,
            "total_categories": total_categories,
            "total_countries": total_countries,
            "updated_today": updated_today,
            "last_sync": last_sync,
            "generated_at": now_utc
        }
        
        # Replace dashboard summary
        db.dashboard_summary.delete_many({})
        db.dashboard_summary.insert_one(dashboard_doc)
        logger.info("Dashboard Summary Generated: %s", dashboard_doc)

        # 2. Generate Country Summary
        logger.info("Generating Country Summary...")
        country_pipeline = [
            {
                "$group": {
                    "_id": {
                        "country": "$country",
                        "category": "$category.name"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": "$_id.country",
                    "total_events": {"$sum": "$count"},
                    "categories": {
                        "$push": {
                            "k": "$_id.category",
                            "v": "$count"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "country": "$_id",
                    "total_events": 1,
                    "categories": {"$arrayToObject": "$categories"},
                    "updated_at": {"$literal": now_utc}
                }
            }
        ]
        
        country_results = list(db.events.aggregate(country_pipeline))
        if country_results:
            db.country_summary.delete_many({})
            db.country_summary.insert_many(country_results)
        logger.info("Country Summary Generated: Refreshed %d countries.", len(country_results))

        # 3. Generate Category Summary
        logger.info("Generating Category Summary...")
        category_pipeline = [
            {
                "$group": {
                    "_id": "$category.name",
                    "total_events": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$_id",
                    "total_events": 1,
                    "updated_at": {"$literal": now_utc}
                }
            }
        ]
        
        category_results = list(db.events.aggregate(category_pipeline))
        if category_results:
            db.category_summary.delete_many({})
            db.category_summary.insert_many(category_results)
        logger.info("Category Summary Generated: Refreshed %d categories.", len(category_results))

        logger.info("Aggregation Completed: All summaries refreshed successfully.")
        
    except Exception as err:
        logger.error("Aggregation Failed: Error generating summaries: %s", err)

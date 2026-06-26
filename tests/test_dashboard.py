"""Test module for the Aggregation Service and dashboard summary collections."""

from datetime import datetime, timezone
import logging
from backend.utils.logger import setup_logging
from backend.database.mongo import MongoConnection
from backend.services.aggregation import run_aggregation

def test_aggregation() -> None:
    """Verifies aggregation service refreshes summary collections correctly."""
    setup_logging()
    logger = logging.getLogger("test_aggregation")
    logger.info("Starting Aggregation Service test...")

    try:
        # Get DB handle
        db = MongoConnection.get_db()

        # 1. Insert Mock Events for Aggregation testing
        logger.info("Inserting mock events to test aggregation pipelines...")
        events_collection = db["events"]
        
        # Clean up existing test events
        events_collection.delete_many({"event_id": {"$in": ["MOCK_EV_001", "MOCK_EV_002", "MOCK_EV_003"]}})
        
        now = datetime.now(timezone.utc)
        mock_events = [
            {
                "event_id": "MOCK_EV_001",
                "title": "Mock Fire Event",
                "description": "Test wildfire",
                "category": {"id": "wildfires", "name": "Wildfires"},
                "status": "open",
                "country": "Canada",
                "latest_geometry": {"date": "2026-06-26T12:00:00Z", "type": "Point", "latitude": 55.0, "longitude": -115.0},
                "geometry_history": [],
                "sources": [],
                "created_at": now,
                "updated_at": now,
                "sync_id": "test_sync_agg"
            },
            {
                "event_id": "MOCK_EV_002",
                "title": "Mock Fire Event 2",
                "description": "Test wildfire 2",
                "category": {"id": "wildfires", "name": "Wildfires"},
                "status": "open",
                "country": "United States",
                "latest_geometry": {"date": "2026-06-26T12:00:00Z", "type": "Point", "latitude": 45.0, "longitude": -120.0},
                "geometry_history": [],
                "sources": [],
                "created_at": now,
                "updated_at": now,
                "sync_id": "test_sync_agg"
            },
            {
                "event_id": "MOCK_EV_003",
                "title": "Mock Volcano Event",
                "description": "Test volcano eruption",
                "category": {"id": "volcanoes", "name": "Volcanoes"},
                "status": "closed",
                "country": "United States",
                "latest_geometry": {"date": "2026-06-25T12:00:00Z", "type": "Point", "latitude": 19.4, "longitude": -155.2},
                "geometry_history": [],
                "sources": [],
                "created_at": now,
                "updated_at": now,
                "sync_id": "test_sync_agg"
            }
        ]
        
        events_collection.insert_many(mock_events)
        logger.info("Mock events inserted successfully.")

        # 2. Trigger Aggregation Service
        run_aggregation()

        # 3. Verify dashboard_summary
        dashboard_summary_count = db.dashboard_summary.count_documents({})
        logger.info("Dashboard summary documents count: %d", dashboard_summary_count)
        assert dashboard_summary_count == 1
        
        dashboard_doc = db.dashboard_summary.find_one()
        logger.info("Transformed Dashboard Summary Document:")
        logger.info("  Total Events: %d", dashboard_doc.get("total_events"))
        logger.info("  Active Events: %d", dashboard_doc.get("active_events"))
        logger.info("  Total Categories: %d", dashboard_doc.get("total_categories"))
        logger.info("  Total Countries: %d", dashboard_doc.get("total_countries"))
        logger.info("  Updated Today: %d", dashboard_doc.get("updated_today"))
        logger.info("  Last Sync: %s", dashboard_doc.get("last_sync"))
        logger.info("  Generated At: %s", dashboard_doc.get("generated_at"))

        # Assert dashboard metrics
        # Minimum counts: total_events should be at least 3, active_events at least 2, etc.
        assert dashboard_doc["total_events"] >= 3
        assert dashboard_doc["active_events"] >= 2
        assert dashboard_doc["total_categories"] >= 2
        assert dashboard_doc["total_countries"] >= 2
        assert dashboard_doc["updated_today"] >= 3

        # 4. Verify country_summary
        country_docs = list(db.country_summary.find())
        logger.info("Country Summary Documents count: %d", len(country_docs))
        assert len(country_docs) >= 2
        
        # Verify specific country details
        us_summary = db.country_summary.find_one({"country": "United States"})
        assert us_summary is not None
        assert us_summary["total_events"] >= 2
        assert us_summary["categories"].get("Wildfires") >= 1
        assert us_summary["categories"].get("Volcanoes") >= 1
        logger.info("Country Summary validation assertions passed.")

        # 5. Verify category_summary
        category_docs = list(db.category_summary.find())
        logger.info("Category Summary Documents count: %d", len(category_docs))
        assert len(category_docs) >= 2
        
        # Verify specific category details
        wildfire_summary = db.category_summary.find_one({"category": "Wildfires"})
        assert wildfire_summary is not None
        assert wildfire_summary["total_events"] >= 2
        logger.info("Category Summary validation assertions passed.")

        # 6. Clean up mock events
        events_collection.delete_many({"event_id": {"$in": ["MOCK_EV_001", "MOCK_EV_002", "MOCK_EV_003"]}})
        logger.info("Mock events cleaned up from events collection.")
        
        # Re-run aggregation to leave database clean
        run_aggregation()
        logger.info("Clean-up aggregation run complete.")

        logger.info("Aggregation Service verification assertions passed successfully.")

    except Exception as err:
        logger.error("Aggregation Service test failed: %s", err)
        raise
    finally:
        MongoConnection.close()

if __name__ == "__main__":
    test_aggregation()

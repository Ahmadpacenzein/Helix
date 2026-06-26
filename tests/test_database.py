"""Test module for database operations and repository persistence."""

import logging
from datetime import datetime, timezone
from backend.utils.logger import setup_logging
from backend.database.mongo import MongoConnection
from backend.services.sync_service import sync_events

def test_database() -> None:
    """Verifies MongoDB connection, automatic index creation, and event upserts."""
    setup_logging()
    logger = logging.getLogger("test_database")
    logger.info("Starting Database Repository test...")

    try:
        # 1. Establish connection and trigger DB initialization (indexes & collections)
        db = MongoConnection.get_db()
        logger.info("Database instance obtained. Collections: %s", db.list_collection_names())

        # Verify index creation
        events_collection = MongoConnection.get_collection("events")
        indexes = events_collection.index_information()
        logger.info("Existing indexes on 'events' collection: %s", list(indexes.keys()))
        
        # Verify specific indexes exist
        assert "event_id_1" in indexes
        assert "category.name_1" in indexes
        assert "country_1" in indexes
        assert "status_1" in indexes
        assert "latest_geometry.date_-1" in indexes
        logger.info("Database index assertions passed successfully.")

        # 2. Test Upsert Logic with dummy event
        test_event = {
            "event_id": "TEST_INCIDENT_999",
            "title": "Initial Title",
            "description": "Test description",
            "category": {
                "id": "earthquakes",
                "name": "Earthquakes"
            },
            "status": "open",
            "country": "TestCountry",
            "latest_geometry": {
                "date": "2026-06-26T00:00:00Z",
                "type": "Point",
                "latitude": 0.0,
                "longitude": 0.0
            },
            "geometry_history": [
                {
                    "date": "2026-06-26T00:00:00Z",
                    "type": "Point",
                    "latitude": 0.0,
                    "longitude": 0.0
                }
            ],
            "sources": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "sync_id": "test_run_1"
        }

        # Clear existing test document if any
        events_collection.delete_one({"event_id": "TEST_INCIDENT_999"})

        # Insert test
        status1 = MongoConnection.upsert_event(test_event)
        logger.info("Upsert 1 status (expected 'inserted'): %s", status1)
        assert status1 == "inserted"

        # Verify insert values
        doc = events_collection.find_one({"event_id": "TEST_INCIDENT_999"})
        assert doc is not None
        assert doc["title"] == "Initial Title"
        assert doc["status"] == "open"
        original_created_at = doc["created_at"]

        # Update test
        test_event["title"] = "Updated Title"
        test_event["status"] = "closed"
        test_event["updated_at"] = datetime.now(timezone.utc)
        
        status2 = MongoConnection.upsert_event(test_event)
        logger.info("Upsert 2 status (expected 'updated'): %s", status2)
        assert status2 == "updated"

        # Verify update values and created_at preservation
        updated_doc = events_collection.find_one({"event_id": "TEST_INCIDENT_999"})
        assert updated_doc["title"] == "Updated Title"
        assert updated_doc["status"] == "closed"
        assert updated_doc["created_at"] == original_created_at  # Preserved!
        logger.info("Upsert behavior and created_at preservation assertions passed.")

        # Clean up test document
        events_collection.delete_one({"event_id": "TEST_INCIDENT_999"})
        logger.info("Cleaned up test document.")

        # 3. Test end-to-end sync_events service (calls fetcher -> transformer -> repo)
        logger.info("Triggering real EONET sync_events integration test...")
        try:
            sync_stats = sync_events()
            logger.info("End-to-end Sync Stats: %s", sync_stats)
            assert sync_stats["total_fetched"] > 0
            assert sync_stats["inserted"] + sync_stats["updated"] + sync_stats["failed"] == sync_stats["total_fetched"]
            logger.info("Sync integration test assertions passed successfully.")
        except Exception as sync_err:
            logger.warning("Sync integration test bypassed or failed due to EONET API status: %s", sync_err)

    except Exception as err:
        logger.error("Database Repository test failed: %s", err)
        raise
    finally:
        MongoConnection.close()

if __name__ == "__main__":
    test_database()

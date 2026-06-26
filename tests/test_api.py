"""Test module for verifying REST API endpoints."""

import json
import logging
from backend.utils.logger import setup_logging
from backend.database.mongo import MongoConnection
from app import app

def test_rest_api() -> None:
    """Verifies that all Flask routes return appropriate status codes and JSON data."""
    setup_logging()
    logger = logging.getLogger("test_api")
    logger.info("Starting REST API test...")

    # Use Flask's test client
    client = app.test_client()

    try:
        # 1. Populate test data in Mongo to verify endpoints with actual payloads
        db = MongoConnection.get_db()
        events_collection = db["events"]
        
        # Clean up existing test events
        events_collection.delete_many({"event_id": {"$in": ["TEST_API_001", "TEST_API_002"]}})
        db.dashboard_summary.delete_many({})
        db.country_summary.delete_many({})
        db.category_summary.delete_many({})

        # Insert events
        mock_events = [
            {
                "event_id": "TEST_API_001",
                "title": "Severe Earthquake in Chile",
                "category": {"id": "earthquakes", "name": "Earthquakes"},
                "status": "open",
                "country": "Chile",
                "latest_geometry": {"date": "2026-06-26T12:00:00Z", "type": "Point", "latitude": -33.4, "longitude": -70.6},
                "geometry_history": [],
                "sources": [{"id": "USGS", "url": "http://usgs.gov"}],
                "sync_id": "test_api_sync"
            },
            {
                "event_id": "TEST_API_002",
                "title": "Wildfire in California",
                "category": {"id": "wildfires", "name": "Wildfires"},
                "status": "closed",
                "country": "United States",
                "latest_geometry": {"date": "2026-06-25T12:00:00Z", "type": "Point", "latitude": 37.8, "longitude": -122.4},
                "geometry_history": [],
                "sources": [],
                "sync_id": "test_api_sync"
            }
        ]
        events_collection.insert_many(mock_events)

        # Run aggregation to update summaries
        from backend.services.aggregation import run_aggregation
        run_aggregation()

        # 2. Test GET /api/dashboard
        logger.info("Testing GET /api/dashboard...")
        resp = client.get("/api/dashboard")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert data["data"]["total_events"] == 2
        assert data["data"]["active_events"] == 1
        assert data["data"]["total_countries"] == 2
        logger.info("GET /api/dashboard passed.")

        # 3. Test GET /api/events
        logger.info("Testing GET /api/events...")
        resp = client.get("/api/events")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert len(data["data"]) == 2
        logger.info("GET /api/events passed.")

        # 4. Test GET /api/events with filters
        logger.info("Testing GET /api/events?country=Chile...")
        resp = client.get("/api/events?country=Chile")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data["data"]) == 1
        assert data["data"][0]["event_id"] == "TEST_API_001"
        logger.info("GET /api/events?country=Chile passed.")

        # 5. Test GET /api/events/<event_id>
        logger.info("Testing GET /api/events/TEST_API_001...")
        resp = client.get("/api/events/TEST_API_001")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert data["data"]["title"] == "Severe Earthquake in Chile"
        logger.info("GET /api/events/TEST_API_001 passed.")

        # 6. Test GET /api/events/<event_id> (Not Found)
        logger.info("Testing GET /api/events/NON_EXISTENT...")
        resp = client.get("/api/events/NON_EXISTENT")
        assert resp.status_code == 404
        data = json.loads(resp.data)
        assert data["success"] is False
        logger.info("GET /api/events/NON_EXISTENT (404) passed.")

        # 7. Test GET /api/analytics/country
        logger.info("Testing GET /api/analytics/country...")
        resp = client.get("/api/analytics/country")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert len(data["data"]) == 2
        logger.info("GET /api/analytics/country passed.")

        # 8. Test GET /api/analytics/category
        logger.info("Testing GET /api/analytics/category...")
        resp = client.get("/api/analytics/category")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert len(data["data"]) == 2
        logger.info("GET /api/analytics/category passed.")

        # 9. Test GET /api/search
        logger.info("Testing GET /api/search?q=California...")
        resp = client.get("/api/search?q=California")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert len(data["data"]) == 1
        assert data["data"][0]["event_id"] == "TEST_API_002"
        logger.info("GET /api/search?q=California passed.")

        # 10. Test GET /api/timeline
        logger.info("Testing GET /api/timeline...")
        resp = client.get("/api/timeline")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert len(data["data"]) == 2
        logger.info("GET /api/timeline passed.")

        # 11. Test GET /api/sync/status
        logger.info("Testing GET /api/sync/status...")
        resp = client.get("/api/sync/status")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        logger.info("GET /api/sync/status passed.")

        # 12. Clean up test data
        events_collection.delete_many({"event_id": {"$in": ["TEST_API_001", "TEST_API_002"]}})
        run_aggregation()
        logger.info("Cleaned up test data.")

        logger.info("All REST API endpoints verified successfully!")

    except Exception as err:
        logger.error("REST API test failed: %s", err)
        raise

if __name__ == "__main__":
    test_rest_api()

"""Test module for the Data Transformation service."""

import json
import logging
from backend.utils.logger import setup_logging
from backend.services.nasa_fetcher import fetch_events
from backend.services.transformer import transform_event

def test_transformer() -> None:
    """Verifies data transformation from EONET schema to HELIX schema."""
    setup_logging()
    logger = logging.getLogger("test_transformer")
    logger.info("Starting Data Transformation test...")

    # Define a mock EONET event to verify transformation
    mock_raw_event = {
        "id": "MOCK_EVENT_123",
        "title": "Mock Wildfire Incident",
        "description": "A test fire incident",
        "closed": "2026-06-26T12:00:00Z",
        "categories": [
            {
                "id": "wildfires",
                "title": "Wildfires"
            }
        ],
        "sources": [
            {
                "id": "MOCK_SRC",
                "url": "http://example.com"
            }
        ],
        "geometries": [
            {
                "date": "2026-06-25T10:00:00Z",
                "type": "Point",
                "coordinates": [-120.5, 35.5]
            },
            {
                "date": "2026-06-26T11:00:00Z",
                "type": "Point",
                "coordinates": [-120.6, 35.6]
            }
        ]
    }

    logger.info("Raw Mock Event JSON:")
    logger.info(json.dumps(mock_raw_event, indent=2))

    # Transform mock event
    transformed = transform_event(mock_raw_event, sync_id="test_sync_run_001")
    if not transformed:
        logger.error("Mock Event transformation returned None!")
        return

    logger.info("Transformed HELIX Document:")
    # Formatting datetime for logging print
    print_friendly = transformed.copy()
    print_friendly["created_at"] = str(print_friendly["created_at"])
    print_friendly["updated_at"] = str(print_friendly["updated_at"])
    logger.info(json.dumps(print_friendly, indent=2))

    # Assertions / Validations
    assert transformed["event_id"] == "MOCK_EVENT_123"
    assert transformed["title"] == "Mock Wildfire Incident"
    assert transformed["description"] == "A test fire incident"
    assert transformed["category"]["id"] == "wildfires"
    assert transformed["category"]["name"] == "Wildfires"
    assert transformed["status"] == "closed"
    assert transformed["country"] is None
    assert transformed["latest_geometry"]["latitude"] == 35.6
    assert transformed["latest_geometry"]["longitude"] == -120.6
    assert len(transformed["geometry_history"]) == 2
    assert transformed["geometry_history"][0]["latitude"] == 35.5
    assert transformed["geometry_history"][0]["longitude"] == -120.5
    assert transformed["sources"][0]["id"] == "MOCK_SRC"
    assert transformed["sync_id"] == "test_sync_run_001"

    logger.info("Mock Event transformation assertions passed successfully.")

    # Let's test with real live EONET data
    try:
        logger.info("Fetching real EONET data to test transformer...")
        raw_data = fetch_events()
        raw_events = raw_data.get("events", [])
        if raw_events:
            logger.info("Found %d live events. Finding the first valid event to transform...", len(raw_events))
            transformed_count = 0
            for idx, raw_evt in enumerate(raw_events):
                live_transformed = transform_event(raw_evt, sync_id="live_sync_run_001")
                if live_transformed:
                    logger.info("Successfully transformed live event at index %d!", idx)
                    logger.info("Live Event ID: %s", live_transformed["event_id"])
                    logger.info("Live Event Title: %s", live_transformed["title"])
                    logger.info("Live Event Category Name: %s", live_transformed["category"]["name"])
                    logger.info("Live Event Latest Geometry: %s", live_transformed["latest_geometry"])
                    transformed_count += 1
                    break
                else:
                    logger.debug("Skipping invalid/rejected event ID: %s", raw_evt.get("id"))
            if transformed_count == 0:
                logger.warning("No live events were successfully transformed.")
    except Exception as err:
        logger.error("Live event transformation test failed with error: %s", err)

if __name__ == "__main__":
    test_transformer()

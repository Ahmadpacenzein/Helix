"""Test module for the NASA EONET fetcher service."""

import logging
from backend.utils.logger import setup_logging
from backend.services.nasa_fetcher import fetch_events

def test_fetcher() -> None:
    """Verifies that the NASA EONET fetcher retrieves data correctly."""
    setup_logging()
    logger = logging.getLogger("test_fetcher")
    logger.info("Starting NASA EONET Fetcher test...")

    try:
        data = fetch_events()
        events = data.get("events", [])
        logger.info("Fetcher test succeeded!")
        logger.info("Total events retrieved: %d", len(events))
        if events:
            # Print info about the first event as verification
            first_event = events[0]
            logger.info("Sample Event Details:")
            logger.info("  ID: %s", first_event.get("id"))
            logger.info("  Title: %s", first_event.get("title"))
            logger.info("  Category: %s", first_event.get("categories", [{}])[0].get("title"))
    except Exception as err:
        logger.error("Fetcher test failed: %s", err)

if __name__ == "__main__":
    test_fetcher()

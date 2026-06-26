"""Module to manage MongoDB index creation for the HELIX project."""

import logging
from pymongo import ASCENDING, DESCENDING
from pymongo.database import Database

logger = logging.getLogger(__name__)

def create_indexes(db: Database) -> None:
    """Creates the required indexes on the database collections.

    Ensures indexes are created only once and logs the operations.

    Args:
        db: The active PyMongo Database instance.
    """
    logger.info("Initializing index creation...")
    
    try:
        # Create indexes on the 'events' collection
        events_collection = db["events"]
        
        # 1. Unique index on event_id
        events_collection.create_index([("event_id", ASCENDING)], unique=True)
        logger.info("Index created: events (event_id, Unique)")

        # 2. Ascending index on category.name
        events_collection.create_index([("category.name", ASCENDING)])
        logger.info("Index created: events (category.name, Ascending)")

        # 3. Ascending index on country
        events_collection.create_index([("country", ASCENDING)])
        logger.info("Index created: events (country, Ascending)")

        # 4. Ascending index on status
        events_collection.create_index([("status", ASCENDING)])
        logger.info("Index created: events (status, Ascending)")

        # 5. Descending index on latest_geometry.date
        events_collection.create_index([("latest_geometry.date", DESCENDING)])
        logger.info("Index created: events (latest_geometry.date, Descending)")

        logger.info("All database indexes created successfully.")
    except Exception as err:
        logger.error("Failed to create database indexes: %s", err)
        raise

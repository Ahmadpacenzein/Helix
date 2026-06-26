"""MongoDB connection manager module.

Handles connection to the MongoDB instance and exposes the database client
and database object. Failures to connect are handled gracefully without
crashing the hosting application.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError, PyMongoError
from config import Config

logger = logging.getLogger(__name__)

class MongoConnection:
    """Manages the lifecycle of the MongoDB connection client."""

    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    @classmethod
    def get_client(cls) -> MongoClient:
        """Initializes and returns the MongoClient instance.

        Verifies the connection by pinging the database. If connection fails,
        logs the error and raises a ConnectionError.

        Returns:
            MongoClient: The active MongoDB client instance.

        Raises:
            ConnectionError: If connection to MongoDB fails or times out.
        """
        if cls._client is None:
            try:
                # serverSelectionTimeoutMS is set to 5000ms to fail quickly if down
                cls._client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
                # Force connection/ping validation
                cls._client.admin.command("ping")
                logger.info("MongoDB client connected successfully to %s", Config.MONGO_URI)
            except Exception as err:
                logger.error("Failed to establish MongoDB connection: %s", err)
                cls._client = None
                raise ConnectionError(f"Cannot connect to MongoDB: {err}") from err
        return cls._client

    @classmethod
    def get_db(cls) -> Database:
        """Retrieves the active database instance.

        Returns:
            Database: The active Database instance.

        Raises:
            ConnectionError: If the client connection cannot be established.
        """
        if cls._db is None:
            client = cls.get_client()
            cls._db = client[Config.DATABASE_NAME]
            # Automatically create collections and indexes
            from backend.database.indexes import create_indexes
            create_indexes(cls._db)
        return cls._db

    @classmethod
    def get_collection(cls, name: str) -> Collection:
        """Retrieves a specific collection from the database.

        Args:
            name: The name of the collection.

        Returns:
            Collection: The collection instance.
        """
        return cls.get_db()[name]

    @classmethod
    def upsert_event(cls, event_doc: Dict[str, Any]) -> str:
        """Upserts an event document into the 'events' collection.

        If the event_id exists, updates the document (preserving created_at).
        If the event_id does not exist, inserts a new document.

        Args:
            event_doc: Transformed HELIX event document.

        Returns:
            str: "inserted" if it is a new document, or "updated" if modified.

        Raises:
            ConnectionError: If database connection fails.
            ValueError: If event_doc is missing event_id or duplicate key error occurs.
        """
        try:
            collection = cls.get_collection("events")
            event_id = event_doc.get("event_id")
            if not event_id:
                raise ValueError("event_doc must contain event_id")

            # Prepare update document preserving created_at
            now = event_doc.get("updated_at") or datetime.now(timezone.utc)
            update_data = {
                "$set": {
                    "title": event_doc.get("title"),
                    "description": event_doc.get("description"),
                    "category": event_doc.get("category"),
                    "status": event_doc.get("status"),
                    "country": event_doc.get("country"),
                    "latest_geometry": event_doc.get("latest_geometry"),
                    "geometry_history": event_doc.get("geometry_history"),
                    "sources": event_doc.get("sources"),
                    "updated_at": now,
                    "sync_id": event_doc.get("sync_id")
                },
                "$setOnInsert": {
                    "created_at": event_doc.get("created_at") or now
                }
            }

            result = collection.update_one(
                {"event_id": event_id},
                update_data,
                upsert=True
            )

            if result.upserted_id is not None or result.matched_count == 0:
                logger.info("Document Inserted: Event ID: %s", event_id)
                return "inserted"
            else:
                logger.info("Document Updated: Event ID: %s", event_id)
                return "updated"

        except DuplicateKeyError as err:
            logger.error("Duplicate Key Error during upsert of event ID %s: %s", event_doc.get("event_id"), err)
            raise ValueError(f"Duplicate key violation: {err}") from err
        except PyMongoError as err:
            logger.error("Database Error during upsert of event ID %s: %s", event_doc.get("event_id"), err)
            raise ConnectionError(f"Database write failed: {err}") from err

    @classmethod
    def close(cls) -> None:
        """Closes the active MongoDB connection."""
        if cls._client is not None:
            cls._client.close()
            logger.info("MongoDB connection closed.")
            cls._client = None
            cls._db = None


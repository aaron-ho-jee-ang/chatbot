import logging
import os
from datetime import datetime, timezone

from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)

_client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017"))
_db = _client["chatbot"]
_collection = _db["messages"]

# Compound index for efficient history retrieval
try:
    _collection.create_index([("session_id", ASCENDING), ("timestamp", ASCENDING)])
except PyMongoError as exc:
    logger.warning("Could not create index at startup: %s", exc)


def save_message(session_id: str, role: str, text: str, language: str, timestamp: datetime) -> None:
    """Insert a message document into the messages collection.

    Logs and swallows any PyMongoError so the request never fails due to
    persistence issues (Requirement 5.3).
    """
    try:
        _collection.insert_one({
            "session_id": session_id,
            "role": role,
            "text": text,
            "language": language,
            "timestamp": timestamp,
        })
    except PyMongoError as exc:
        logger.error("Failed to save message for session %s: %s", session_id, exc)


def get_messages(session_id: str) -> list:
    """Return all messages for a session sorted by timestamp ascending."""
    cursor = _collection.find(
        {"session_id": session_id},
        {"_id": 0},
        sort=[("timestamp", ASCENDING)],
    )
    return list(cursor)

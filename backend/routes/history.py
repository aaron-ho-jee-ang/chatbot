"""History endpoint."""

from flask import Blueprint, jsonify

from services import conversation_store

history_bp = Blueprint("history", __name__)


@history_bp.get("/api/history/<session_id>")
def get_history(session_id: str):
    messages = conversation_store.get_messages(session_id)

    # Convert datetime timestamps to ISO format strings for JSON serialization
    for msg in messages:
        if "timestamp" in msg and hasattr(msg["timestamp"], "isoformat"):
            msg["timestamp"] = msg["timestamp"].isoformat()

    return jsonify(messages), 200

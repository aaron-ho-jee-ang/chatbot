"""Chat and health endpoints."""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from services import conversation_store, language_detector, llm_client

chat_bp = Blueprint("chat", __name__)


@chat_bp.post("/api/chat")
def post_chat():
    data = request.get_json(silent=True) or {}

    session_id = data.get("session_id")
    message = data.get("message")

    if not session_id or not message:
        return jsonify({"error": "Missing required fields: session_id and message"}), 400

    language = language_detector.detect(message)

    # Persist user message before calling LLM
    conversation_store.save_message(
        session_id=session_id,
        role="user",
        text=message,
        language=language,
        timestamp=datetime.now(timezone.utc),
    )

    try:
        response_text = llm_client.generate(prompt=message, language=language)
    except Exception as exc:
        return jsonify({"error": f"LLM service unavailable: {exc}"}), 503

    # Persist assistant message after receiving response
    conversation_store.save_message(
        session_id=session_id,
        role="assistant",
        text=response_text,
        language=language,
        timestamp=datetime.now(timezone.utc),
    )

    return jsonify({"response": response_text, "language": language, "session_id": session_id}), 200


@chat_bp.get("/api/health")
def get_health():
    return jsonify({"status": "ok"}), 200

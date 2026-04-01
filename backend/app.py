import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from routes.chat import chat_bp
from routes.history import history_bp

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# --- Required environment variable checks ---

llm_api_key = os.environ.get("LLM_API_KEY")
llm_model_path = os.environ.get("LLM_MODEL_PATH")

if not llm_api_key and not llm_model_path:
    logger.error(
        "Missing required environment variable: set LLM_API_KEY (for an "
        "OpenAI-compatible API) or LLM_MODEL_PATH (for a local model)."
    )
    sys.exit(1)

mongodb_uri = os.environ.get("MONGODB_URI")
if not mongodb_uri:
    logger.error(
        "Missing required environment variable: MONGODB_URI must be set to a "
        "valid MongoDB connection string (e.g. mongodb://localhost:27017/chatbot)."
    )
    sys.exit(1)

# --- Flask app ---

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_bp)
app.register_blueprint(history_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

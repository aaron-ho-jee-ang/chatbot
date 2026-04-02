# Multilingual Chatbot

A multilingual chatbot that detects the language of your message and responds in kind. Built with Next.js (frontend), Flask (backend), MongoDB (persistence), and Cloudflared (public tunnel). Everything runs via Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (v2+)

## Setup

**1. Clone the repository**

```bash
git clone <repository-url>
cd chatbot
```

**2. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and fill in the required values:

| Variable | Description |
|---|---|
| `LLM_API_KEY` | API key for an OpenAI-compatible LLM service |
| `LLM_MODEL_PATH` | Path to a local model file (alternative to `LLM_API_KEY`) |
| `MONGODB_URI` | MongoDB connection string (default works for local Docker setup) |
| `NEXT_PUBLIC_API_URL` | Base URL of the Flask backend (default: `http://localhost:5000`) |

> Provide either `LLM_API_KEY` (cloud) or `LLM_MODEL_PATH` (local) — not both.

**3. Start the application**

```bash
docker compose up
```

This builds and starts all services: MongoDB, Flask backend, Next.js frontend, and Cloudflared tunnel.

## Accessing the App

Once all services are healthy, open your browser at:

```
http://localhost:3000
```

The Flask backend API is available at `http://localhost:5000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | Send a message; returns LLM response and detected language |
| `GET` | `/api/history/:id` | Retrieve conversation history for a session ID |
| `GET` | `/api/health` | Health check — returns `{"status": "ok"}` |

### POST /api/chat

Request body:
```json
{ "session_id": "uuid-v4", "message": "Hello!" }
```

Response:
```json
{ "response": "Hello! How can I help?", "language": "en", "session_id": "uuid-v4" }
```

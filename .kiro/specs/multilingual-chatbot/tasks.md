# Implementation Plan: Multilingual Chatbot

## Overview

Incremental implementation of the multilingual chatbot: Flask backend first (env config, language detection, LLM client, persistence, REST routes), then the Next.js frontend (session management, chat UI, API client), and finally Docker/deployment wiring.

## Tasks

- [x] 1. Bootstrap project structure and environment configuration
  - Create the top-level directory layout: `backend/`, `frontend/`, `docker-compose.yml`, `.env.example`
  - In `backend/app.py`, read `LLM_API_KEY` (or `LLM_MODEL_PATH`) and `MONGODB_URI` from environment at startup; log a descriptive error and `sys.exit(1)` if any required variable is absent
  - Create `backend/requirements.txt` with `flask`, `langdetect`, `openai`, `pymongo`, `python-dotenv`
  - Create `.env.example` listing `LLM_API_KEY`, `LLM_MODEL_PATH`, `MONGODB_URI`, `NEXT_PUBLIC_API_URL` with placeholder values and inline comments
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 2. Implement language detection service
  - [x] 2.1 Create `backend/services/language_detector.py`
    - Implement `detect(text: str) -> str` wrapping `langdetect.detect()`
    - Return a BCP 47 language code; catch `LangDetectException` and low-confidence results, falling back to `"en"`
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ]* 2.2 Write property test for language detector
    - **Property 1: Fallback to English on empty or undetectable input**
    - **Validates: Requirements 2.3**

  - [ ]* 2.3 Write unit tests for language detector
    - Test detection of at least 10 languages (en, fr, es, de, ar, zh-cn, ja, pt, it, hi)
    - Test fallback to `"en"` on empty string and exception path
    - _Requirements: 2.2, 2.3_

- [x] 3. Implement LLM client service
  - [x] 3.1 Create `backend/services/llm_client.py`
    - Implement `generate(prompt: str, language: str) -> str`
    - Build a system message instructing the LLM to reply in `language`, then pass the user prompt
    - Call the OpenAI-compatible API using `LLM_API_KEY`; raise a descriptive exception on API error
    - Truncate the response to 2000 characters and append a truncation notice if exceeded
    - _Requirements: 3.1, 3.2, 3.4, 3.5_

  - [ ]* 3.2 Write property test for LLM client truncation
    - **Property 2: Response never exceeds 2000 characters after truncation**
    - **Validates: Requirements 3.5**

  - [ ]* 3.3 Write unit tests for LLM client
    - Test truncation boundary (exactly 2000, 2001, and 1999 chars)
    - Test that a 503-worthy exception is raised when the API returns an error
    - _Requirements: 3.4, 3.5_

- [x] 4. Implement conversation store service
  - [x] 4.1 Create `backend/services/conversation_store.py`
    - Implement `save_message(session_id, role, text, language, timestamp)` — insert into `messages` collection; catch and log any `PyMongoError` without re-raising
    - Implement `get_messages(session_id) -> list` — return documents sorted by `timestamp` ascending
    - Create a compound index on `{ session_id: 1, timestamp: 1 }` at module initialisation
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ]* 4.2 Write property test for conversation store ordering
    - **Property 3: Messages returned by `get_messages` are always in ascending timestamp order**
    - **Validates: Requirements 5.4**

  - [ ]* 4.3 Write unit tests for conversation store
    - Test that a DB error in `save_message` is swallowed and logged (does not raise)
    - Test `get_messages` returns an empty list for an unknown session
    - _Requirements: 5.3_

- [x] 5. Implement Flask REST routes
  - [x] 5.1 Create `backend/routes/chat.py` with `POST /api/chat` and `GET /api/health`
    - Validate that `session_id` and `message` are present; return HTTP 400 with `{ "error": "..." }` if missing
    - Call `language_detector.detect()`, `llm_client.generate()`, `conversation_store.save_message()` for both user and assistant turns
    - Return HTTP 200 `{ "response", "language", "session_id" }` on success
    - Return HTTP 503 `{ "error": "..." }` when the LLM service raises an exception
    - `GET /api/health` returns `{ "status": "ok" }`
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 3.3, 3.4_

  - [x] 5.2 Create `backend/routes/history.py` with `GET /api/history/<session_id>`
    - Call `conversation_store.get_messages(session_id)` and return the list as JSON with HTTP 200
    - _Requirements: 5.4, 7.1_

  - [x] 5.3 Register blueprints in `backend/app.py` and wire env-var startup checks
    - _Requirements: 9.1, 9.2, 9.3_

  - [ ]* 5.4 Write integration tests for REST routes
    - Test `POST /api/chat` happy path, missing fields (400), and LLM error (503)
    - Test `GET /api/health` returns 200
    - Test `GET /api/history/<session_id>` returns messages in order
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 5.4_

- [x] 6. Checkpoint — backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Scaffold Next.js frontend and API client
  - [x] 7.1 Initialise the Next.js app in `frontend/` (TypeScript, App Router)
    - Add `uuid` dependency for session ID generation
    - _Requirements: 6.1_

  - [x] 7.2 Create `frontend/src/lib/api.ts`
    - Implement `sendMessage(sessionId: string, message: string): Promise<ChatResponse>`
    - Implement `getHistory(sessionId: string): Promise<Message[]>`
    - Read base URL from `NEXT_PUBLIC_API_URL`, defaulting to `http://localhost:5000`
    - _Requirements: 7.1, 7.2_

  - [ ]* 7.3 Write unit tests for `api.ts`
    - Test that `sendMessage` serialises the request body correctly
    - Test that a non-200 response rejects the promise
    - _Requirements: 7.1, 7.2_

- [x] 8. Implement chat UI components
  - [x] 8.1 Create `MessageBubble` component
    - Render user and assistant messages with visually distinct styles
    - Display the BCP 47 language code badge on assistant messages
    - _Requirements: 4.2, 4.3_

  - [x] 8.2 Create `MessageList` component
    - Render a scrollable list of `MessageBubble` components
    - Auto-scroll to the latest message using `useEffect` and a bottom-anchor ref
    - _Requirements: 4.1, 4.4_

  - [x] 8.3 Create `InputBar` component
    - Controlled text input + send button
    - Disable send and show a loading spinner while `loading === true`
    - Prevent submission when input is empty; show an inline validation message
    - _Requirements: 1.1, 1.3, 1.4_

  - [ ]* 8.4 Write unit tests for UI components
    - Test `InputBar` blocks empty submission and shows validation message
    - Test `MessageBubble` renders language badge only on assistant messages
    - _Requirements: 1.4, 4.3_

- [x] 9. Implement `ChatPage` and session management
  - [x] 9.1 Create `frontend/src/app/page.tsx` as the `ChatPage` component
    - On mount, read session ID from `sessionStorage`; generate a UUID v4 and persist it if absent
    - Hold `messages: Message[]` and `loading: boolean` in state
    - On send: set `loading = true`, call `sendMessage`, append user + assistant messages to state, set `loading = false`
    - Render `MessageList` and `InputBar`
    - _Requirements: 1.2, 6.1, 6.2, 6.3_

  - [ ]* 9.2 Write property test for session ID persistence
    - **Property 4: Session ID read from `sessionStorage` is always the same UUID across multiple sends within the same session**
    - **Validates: Requirements 6.1, 6.3**

  - [ ]* 9.3 Write unit tests for `ChatPage`
    - Test that a session ID is generated and stored on first render
    - Test that the same session ID is reused on subsequent renders
    - Test that the loading state disables the send button during a pending request
    - _Requirements: 6.1, 6.3, 1.3_

- [x] 10. Checkpoint — frontend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Add Docker configuration
  - [x] 11.1 Create `backend/Dockerfile`
    - Install Python dependencies from `requirements.txt` and start the Flask server
    - _Requirements: 8.1_

  - [x] 11.2 Create `frontend/Dockerfile`
    - Build the Next.js application and start the production server
    - _Requirements: 8.2_

  - [x] 11.3 Create `docker-compose.yml`
    - Define services: `frontend` (port 3000), `backend` (port 5000), `mongodb`, `cloudflared`
    - Pass environment variables to each service; mount `.env` for secrets
    - _Requirements: 8.3, 8.4_

- [x] 12. Write README
  - Create `README.md` with step-by-step instructions for cloning the repo, configuring environment variables, and running with `docker compose up`
  - _Requirements: 8.5_

- [x] 13. Final checkpoint — all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at the backend and frontend boundaries
- Property tests validate universal correctness properties; unit tests cover specific examples and edge cases

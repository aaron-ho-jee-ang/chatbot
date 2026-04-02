# Requirements Document

## Introduction

A multilingual chatbot application that accepts user text input, detects the language of the input, and responds using an LLM in the same language. The system is composed of a Next.js frontend, a Flask backend API, a MongoDB database for persisting conversations, and is deployed via Docker with Cloudflared Quick Tunnel for public access.

## Glossary

- **Chatbot**: The full-stack application enabling users to converse with an LLM.
- **Frontend**: The Next.js web application that renders the chat UI and communicates with the Backend.
- **Backend**: The Flask Python API that handles requests, invokes the LLM, and persists data.
- **LLM**: The language model (locally installed or API-based) responsible for generating responses.
- **Language_Detector**: The component within the Backend that identifies the language of user input.
- **Conversation_Store**: The MongoDB collection that persists chat messages and metadata.
- **Message**: A single user or assistant turn in a conversation, including text, detected language, and timestamp.
- **Session**: A logical grouping of Messages belonging to one continuous chat interaction.
- **Tunnel**: The Cloudflared Quick Tunnel that exposes the application to the public internet.

---

## Requirements

### Requirement 1: Accept and Display User Input

**User Story:** As a user, I want to type a message and send it to the chatbot, so that I can start a conversation.

#### Acceptance Criteria

1. THE Frontend SHALL render a text input field and a send button on the chat interface.
2. WHEN the user submits a message (via button click or Enter key), THE Frontend SHALL send the message text to the Backend via an HTTP POST request.
3. WHILE a response is pending, THE Frontend SHALL display a loading indicator and disable the send button.
4. IF the message text is empty, THEN THE Frontend SHALL prevent submission and display an inline validation message.

---

### Requirement 2: Language Detection

**User Story:** As a user, I want the chatbot to detect the language I am writing in, so that it can respond in the same language without me having to configure anything.

#### Acceptance Criteria

1. WHEN the Backend receives a message, THE Language_Detector SHALL identify the language of the message text.
2. THE Language_Detector SHALL support detection of at least 10 languages, including English, French, Spanish, German, Arabic, Chinese (Simplified), Japanese, Portuguese, Italian, and Hindi.
3. IF the Language_Detector cannot determine the language with sufficient confidence, THEN THE Backend SHALL default to English for the LLM prompt.
4. THE Backend SHALL include the detected language code (BCP 47 format) in the response payload returned to the Frontend.

---

### Requirement 3: LLM Response Generation

**User Story:** As a user, I want the chatbot to reply to my message using an LLM, so that I receive a meaningful, context-aware answer.

#### Acceptance Criteria

1. WHEN the Backend receives a message, THE Backend SHALL construct a prompt that instructs the LLM to respond in the detected language.
2. THE Backend SHALL send the constructed prompt to the LLM and receive a generated response.
3. WHEN the LLM returns a response, THE Backend SHALL return the response text and detected language code to the Frontend within 30 seconds.
4. IF the LLM service is unavailable or returns an error, THEN THE Backend SHALL return an HTTP 503 response with a descriptive error message.
5. IF the LLM response exceeds 2000 characters, THEN THE Backend SHALL truncate the response to 2000 characters and append a truncation notice.

---

### Requirement 4: Display Chatbot Response

**User Story:** As a user, I want to see the chatbot's reply in the chat window, so that I can read the response and continue the conversation.

#### Acceptance Criteria

1. WHEN the Frontend receives a successful response from the Backend, THE Frontend SHALL append the assistant message to the chat history display.
2. THE Frontend SHALL render user messages and assistant messages with visually distinct styles.
3. THE Frontend SHALL display the detected language code alongside each assistant message.
4. WHEN a new message is appended, THE Frontend SHALL scroll the chat window to the latest message.

---

### Requirement 5: Conversation Persistence

**User Story:** As a developer, I want all messages to be stored in MongoDB, so that conversation history can be retrieved and analysed.

#### Acceptance Criteria

1. WHEN the Backend processes a message, THE Conversation_Store SHALL persist a Message document containing: session ID, role (user or assistant), message text, detected language code, and UTC timestamp.
2. THE Conversation_Store SHALL store user and assistant messages as separate documents within the same Session.
3. IF the Conversation_Store is unavailable, THEN THE Backend SHALL log the error and continue processing the LLM response without failing the request.
4. THE Backend SHALL expose a GET endpoint at `/api/history/{session_id}` that returns all Messages for a given Session in chronological order.

---

### Requirement 6: Session Management

**User Story:** As a user, I want my conversation to be tracked as a session, so that context is maintained across multiple messages.

#### Acceptance Criteria

1. WHEN a user opens the chat interface for the first time, THE Frontend SHALL generate a unique session ID (UUID v4) and store it in the browser's session storage.
2. THE Frontend SHALL include the session ID in every HTTP request sent to the Backend.
3. WHILE a session ID exists in session storage, THE Frontend SHALL reuse the same session ID for subsequent messages.
4. THE Backend SHALL associate every persisted Message with the session ID provided in the request.

---

### Requirement 7: REST API Contract

**User Story:** As a developer, I want a well-defined REST API, so that the Frontend and Backend can integrate reliably.

#### Acceptance Criteria

1. THE Backend SHALL expose a POST endpoint at `/api/chat` that accepts a JSON body with fields `session_id` (string), `message` (string).
2. WHEN a valid request is received, THE Backend SHALL return HTTP 200 with a JSON body containing `response` (string), `language` (string, BCP 47), and `session_id` (string).
3. IF the request body is missing required fields, THEN THE Backend SHALL return HTTP 400 with a JSON body containing a descriptive `error` field.
4. THE Backend SHALL expose a GET endpoint at `/api/health` that returns HTTP 200 with `{"status": "ok"}` when the service is running.

---

### Requirement 8: Containerised Deployment

**User Story:** As a developer, I want the application to run in Docker containers, so that it can be deployed consistently across environments.

#### Acceptance Criteria

1. THE Chatbot SHALL provide a `Dockerfile` for the Backend service that installs all Python dependencies and starts the Flask server.
2. THE Chatbot SHALL provide a `Dockerfile` for the Frontend service that builds the Next.js application and starts the production server.
3. THE Chatbot SHALL provide a `docker-compose.yml` that orchestrates the Frontend, Backend, MongoDB, and Cloudflared Tunnel services.
4. WHEN `docker compose up` is executed, THE Chatbot SHALL start all services and make the Frontend accessible on port 3000 and the Backend on port 5000.
5. THE Chatbot SHALL provide a `README.md` with step-by-step instructions for cloning the repository, configuring environment variables, and running the application with Docker Compose.

---

### Requirement 9: Environment Configuration

**User Story:** As a developer, I want all secrets and environment-specific values to be managed via environment variables, so that the application is secure and portable.

#### Acceptance Criteria

1. THE Backend SHALL read the LLM API key or model path from an environment variable named `LLM_API_KEY` or `LLM_MODEL_PATH` respectively.
2. THE Backend SHALL read the MongoDB connection string from an environment variable named `MONGODB_URI`.
3. IF a required environment variable is missing at startup, THEN THE Backend SHALL log a descriptive error and exit with a non-zero status code.
4. THE Chatbot SHALL provide a `.env.example` file listing all required environment variables with placeholder values and inline comments.

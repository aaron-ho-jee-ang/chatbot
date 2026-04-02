const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:5000";

export interface ChatResponse {
  response: string;
  language: string;
  session_id: string;
}

export interface Message {
  role: "user" | "assistant";
  text: string;
  language: string;
  timestamp: string;
}

export async function sendMessage(
  sessionId: string,
  message: string
): Promise<ChatResponse> {
  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });

  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status} ${res.statusText}`);
  }

  return res.json() as Promise<ChatResponse>;
}

export async function getHistory(sessionId: string): Promise<Message[]> {
  const res = await fetch(`${BASE_URL}/api/history/${sessionId}`);

  if (!res.ok) {
    throw new Error(`History request failed: ${res.status} ${res.statusText}`);
  }

  return res.json() as Promise<Message[]>;
}

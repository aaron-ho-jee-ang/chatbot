'use client';

import { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import MessageList from '../components/MessageList';
import InputBar from '../components/InputBar';
import { sendMessage } from '../lib/api';

interface UIMessage {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  language?: string;
}

export default function ChatPage() {
  const [sessionId, setSessionId] = useState<string>('');
  const [messages, setMessages] = useState<UIMessage[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let id = sessionStorage.getItem('session_id');
    if (!id) {
      id = uuidv4();
      sessionStorage.setItem('session_id', id);
    }
    setSessionId(id);
  }, []);

  const handleSend = async (message: string) => {
    const userMsg: UIMessage = {
      id: uuidv4(),
      role: 'user',
      text: message,
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const data = await sendMessage(sessionId, message);
      const assistantMsg: UIMessage = {
        id: uuidv4(),
        role: 'assistant',
        text: data.response,
        language: data.language,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg: UIMessage = {
        id: uuidv4(),
        role: 'assistant',
        text: 'Sorry, something went wrong. Please try again.',
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <MessageList messages={messages} />
      </div>
      <InputBar onSend={handleSend} loading={loading} />
    </div>
  );
}

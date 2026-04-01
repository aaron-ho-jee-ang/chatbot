'use client';

import React, { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

interface UIMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
  language?: string;
}

interface MessageListProps {
  messages: UIMessage[];
}

export default function MessageList({ messages }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const containerStyle: React.CSSProperties = {
    overflowY: "auto",
    maxHeight: "calc(100vh - 160px)",
    padding: "16px",
    display: "flex",
    flexDirection: "column",
  };

  return (
    <div style={containerStyle}>
      {messages.map((msg) => (
        <MessageBubble
          key={msg.id}
          role={msg.role}
          text={msg.text}
          language={msg.language}
        />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}

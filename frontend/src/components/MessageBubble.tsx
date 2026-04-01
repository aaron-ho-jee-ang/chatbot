import React from "react";

interface MessageBubbleProps {
  role: "user" | "assistant";
  text: string;
  language?: string;
}

export default function MessageBubble({ role, text, language }: MessageBubbleProps) {
  const isUser = role === "user";

  const containerStyle: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    alignItems: isUser ? "flex-end" : "flex-start",
    marginBottom: "12px",
  };

  const bubbleStyle: React.CSSProperties = {
    maxWidth: "70%",
    padding: "10px 14px",
    borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
    backgroundColor: isUser ? "#2563eb" : "#f3f4f6",
    color: isUser ? "#ffffff" : "#111827",
    fontSize: "15px",
    lineHeight: "1.5",
    wordBreak: "break-word",
  };

  const badgeStyle: React.CSSProperties = {
    marginTop: "4px",
    fontSize: "11px",
    color: "#6b7280",
    backgroundColor: "#e5e7eb",
    borderRadius: "4px",
    padding: "1px 6px",
    alignSelf: "flex-start",
  };

  return (
    <div style={containerStyle}>
      <div style={bubbleStyle}>{text}</div>
      {!isUser && language && (
        <span style={badgeStyle}>{language}</span>
      )}
    </div>
  );
}

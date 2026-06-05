"use client";

import { useState } from "react";
import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import { sendMessage } from "@/services/chat.service";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello 👋 Ask anything from your documents.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;

    // 1. Add user message
    const userMessage: Message = {
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      // 2. Call backend
      const res = await sendMessage(text);

      // 3. IMPORTANT FIX: extract response correctly
      const botMessage: Message = {
        role: "assistant",
        content: res.response || "No response received",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Error while fetching AI response",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            role={msg.role}
            content={msg.content}
          />
        ))}

        {loading && (
          <div className="text-gray-500 text-sm animate-pulse">
            AI is thinking...
          </div>
        )}
      </div>

      {/* INPUT AREA */}
      <div className="border-t bg-white p-3">
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}
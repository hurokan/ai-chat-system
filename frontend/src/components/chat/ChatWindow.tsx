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

  // One session per browser tab/chat
  const [sessionId] = useState(
    crypto.randomUUID()
  );

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello 👋 Ask anything from your documents.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const handleSend = async (
    text: string
  ) => {

    console.log(
      "🟡 handleSend triggered:",
      text
    );

    if (!text.trim()) {
      return;
    }

    const userMessage: Message = {
      role: "user",
      content: text,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    setLoading(true);

    try {

      console.log(
        "SESSION ID:",
        sessionId
      );

      const res = await sendMessage(
        text,
        sessionId
      );

      console.log(
        "DEBUG API RESPONSE:",
        res
      );

      const answer =
        res?.response ||
        res?.answer ||
        "No response received";

      const botMessage: Message = {
        role: "assistant",
        content: answer,
      };

      setMessages((prev) => [
        ...prev,
        botMessage,
      ]);

    } catch (error) {

      console.error(
        "Chat error:",
        error
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Error while fetching AI response",
        },
      ]);

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">

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

      <div className="border-t bg-white p-3">
        <ChatInput
          onSend={handleSend}
        />
      </div>

    </div>
  );
}
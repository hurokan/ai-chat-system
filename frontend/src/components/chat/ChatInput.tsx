"use client";

import { useState } from "react";

export default function ChatInput({
  onSend,
}: {
  onSend: (msg: string) => void;
}) {
  const [message, setMessage] = useState("");

  const submit = () => {
    if (!message.trim()) return;

    onSend(message);
    setMessage("");
  };

  return (
    <div className="border-t p-4 flex gap-2">
      <input
        value={message}
        onChange={(e) =>
          setMessage(e.target.value)
        }
        className="flex-1 border rounded-lg p-3"
        placeholder="Ask anything..."
      />

      <button
        onClick={submit}
        className="bg-blue-600 text-white px-4 rounded-lg"
      >
        Send
      </button>
    </div>
  );
}

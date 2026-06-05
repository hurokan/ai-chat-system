"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Props {
  role: string;
  content: string;
}

export default function ChatMessage({
  role,
  content,
}: Props) {
  return (
    <div
      className={`flex mb-4 ${
        role === "user"
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`max-w-[75%] rounded-xl p-4 ${
          role === "user"
            ? "bg-blue-600 text-white"
            : "bg-gray-100 text-black"
        }`}
      >
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
        >
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}

"use client";

import { useState } from "react";
import ChatBot from "@/components/chat/ChatBot";
import ChatBotIcon from "@/components/chat/ChatBotIcon";

export default function ChatPage() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Main content can go here */}
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Chat with AI Assistant
        </h1>
        <p className="text-gray-600 mb-8">
          Manage your tasks using natural language conversations.
        </p>

        {/* Instructions */}
        <div className="bg-white rounded-xl shadow-sm p-6 max-w-2xl">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            How to use
          </h2>
          <ul className="space-y-3 text-gray-600">
            <li className="flex items-start gap-3">
              <span className="shrink-0 w-6 h-6 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-sm font-medium">
                1
              </span>
              <span>Click the chat icon in the bottom-right corner to open the chat</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="shrink-0 w-6 h-6 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-sm font-medium">
                2
              </span>
              <span>Type naturally: "Add a task to buy groceries"</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="shrink-0 w-6 h-6 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-sm font-medium">
                3
              </span>
              <span>Ask to see your tasks: "Show me my pending tasks"</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="shrink-0 w-6 h-6 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-sm font-medium">
                4
              </span>
              <span>Complete tasks: "Mark task 1 as complete"</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Chat components */}
      <ChatBot isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
      <ChatBotIcon
        isOpen={isChatOpen}
        onClick={() => setIsChatOpen(!isChatOpen)}
        hasNewMessage={false}
      />
    </div>
  );
}

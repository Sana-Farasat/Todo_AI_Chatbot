"use client";

import { useState, ReactNode } from "react";
import ChatBot from "@/components/chat/ChatBot";
import ChatBotIcon from "@/components/chat/ChatBotIcon";

export default function ChatBotWrapper({ children }: { children: ReactNode }) {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <>
      {children}
      <ChatBot isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
      <ChatBotIcon
        isOpen={isChatOpen}
        onClick={() => setIsChatOpen(!isChatOpen)}
        hasNewMessage={false}
      />
    </>
  );
}

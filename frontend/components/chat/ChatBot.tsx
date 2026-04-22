"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Send, Loader2 } from "lucide-react";
import useApi from "@/lib/api";
import { useAuth } from "@/lib/auth";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

interface Message {
  id?: number;
  role: "user" | "assistant" | "system";
  content: string;
  created_at?: string;
  tool_calls?: any[];
}

interface ChatBotProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ChatBot({ isOpen, onClose }: ChatBotProps) {
  const api = useApi();
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversation history on mount
  useEffect(() => {
    if (isOpen && user && messages.length === 0) {
      loadConversationHistory();
    }
  }, [isOpen, user]);

  const loadConversationHistory = async () => {
    if (!user) return;
    
    try {
      // const history = await api.getChatHistory(user);
      const history = await api.getChatHistory();
      if (history && history.length > 0) {
        // Get the most recent conversation
        const latestConv = history[0];
        setConversationId(latestConv.id);
        
        // Load messages for this conversation
        // const messages = await api.getChatHistory(user, latestConv.id);
        const messages = await api.getChatHistory(latestConv.id);
        setMessages(messages.map((m: any) => ({
          id: m.id,
          role: m.role as "user" | "assistant" | "system",
          content: m.content,
          created_at: m.created_at,
        })));
      }
    } catch (error) {
      console.error("Failed to load conversation history:", error);
    }
  };

  const sendMessage = async (content: string) => {
    if (!user || !content.trim()) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      role: "user",
      content: content.trim(),
      created_at: new Date().toISOString(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // const response = await api.chat(user, content, conversationId || undefined);
      const response = await api.chat(content, conversationId || undefined);
      
      // Update conversation ID if this is a new conversation
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response
      const assistantMessage: Message = {
        role: "assistant",
        content: response.response,
        created_at: new Date().toISOString(),
        tool_calls: response.tool_calls,
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error("Chat error:", error);
      
      // Add error message
      const errorMessage: Message = {
        role: "assistant",
        content: `Sorry, I encountered an error: ${error.message || "Please try again"}`,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  if (!user) {
    return null;
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Chat Window */}
          <motion.div
            className="fixed bottom-24 right-6 w-95 h-150 max-h-[80vh] bg-white rounded-2xl shadow-2xl flex flex-col z-50 overflow-hidden"
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
          >
            {/* Header */}
            <div className="bg-linear-to-r from-amber-600 to-yellow-600 px-4 py-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                <div>
                  <h3 className="text-white font-semibold">AI Assistant</h3>
                  <p className="text-purple-200 text-xs">Powered by Gemini AI</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {messages.length > 0 && (
                  <button
                    onClick={clearConversation}
                    className="text-purple-200 hover:text-white text-xs px-2 py-1 rounded hover:bg-white/10 transition-colors"
                  >
                    Clear
                  </button>
                )}
                <button
                  onClick={onClose}
                  className="text-white hover:bg-white/10 p-2 rounded-full transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-gray-500">
                  <MessageCircle className="w-12 h-12 mb-3 opacity-20" />
                  <p className="text-sm text-center">
                    Hi! I'm your AI assistant.<br />
                    Ask me to help manage your tasks!
                  </p>
                  <div className="mt-4 space-y-2 text-xs text-gray-400">
                    <p>Try: "Add a task to buy groceries"</p>
                    <p>Try: "Show me my pending tasks"</p>
                    <p>Try: "Mark task 1 as complete"</p>
                  </div>
                </div>
              ) : (
                <>
                  {messages.map((message, index) => (
                    <ChatMessage key={index} message={message} />
                  ))}
                  {isLoading && (
                    <div className="flex items-center gap-2 text-gray-500 text-sm">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>AI is thinking...</span>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>

            {/* Input */}
            <ChatInput onSend={sendMessage} isLoading={isLoading} />
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

// Import MessageCircle for the empty state
function MessageCircle(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z" />
    </svg>
  );
}

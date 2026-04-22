"use client";

import { motion } from "framer-motion";
import { Toolbox, CheckCircle, Trash2, Edit, List } from "lucide-react";

interface Message {
  id?: number;
  role: "user" | "assistant" | "system";
  content: string;
  created_at?: string;
  tool_calls?: any[];
}

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";

  if (isSystem) {
    return (
      <div className="text-center text-xs text-gray-400 my-4">
        {message.content}
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-linear-to-br from-amber-500 to-amber-600 text-white"
            : "bg-white text-gray-800 shadow-sm border border-gray-100"
        }`}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        
        {/* Tool call indicators */}
        {message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200 space-y-2">
            {message.tool_calls.map((toolCall, index) => (
              <ToolCallIndicator key={index} toolCall={toolCall} isUser={isUser} />
            ))}
          </div>
        )}

        {/* Timestamp */}
        {message.created_at && (
          <p
            className={`text-xs mt-2 ${
              isUser ? "text-blue-100" : "text-gray-400"
            }`}
          >
            {formatTimestamp(message.created_at)}
          </p>
        )}
      </div>
    </motion.div>
  );
}

function ToolCallIndicator({ toolCall, isUser }: { toolCall: any; isUser: boolean }) {
  const { tool, result } = toolCall;
  
  const getToolIcon = () => {
    switch (tool) {
      case "add_task":
        return <CheckCircle className="w-4 h-4" />;
      case "delete_task":
        return <Trash2 className="w-4 h-4" />;
      case "update_task":
        return <Edit className="w-4 h-4" />;
      case "list_tasks":
        return <List className="w-4 h-4" />;
      default:
        return <Toolbox className="w-4 h-4" />;
    }
  };

  const isSuccess = result?.success;

  return (
    <div
      className={`flex items-center gap-2 text-xs ${
        isSuccess ? "text-green-600" : "text-red-600"
      }`}
    >
      {getToolIcon()}
      <span>
        {tool === "add_task" && result?.title && (
          <>Added: {result.title}</>
        )}
        {tool === "complete_task" && result?.title && (
          <>Completed: {result.title}</>
        )}
        {tool === "delete_task" && result?.title && (
          <>Deleted: {result.title}</>
        )}
        {tool === "update_task" && (
          <>Updated task</>
        )}
        {tool === "list_tasks" && (
          <>Listed {result?.tasks?.length || 0} tasks</>
        )}
      </span>
    </div>
  );
}

function formatTimestamp(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return "Just now";
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
}

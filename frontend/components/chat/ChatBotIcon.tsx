"use client";

import { motion } from "framer-motion";
import { MessageCircle, X } from "lucide-react";

interface ChatBotIconProps {
  isOpen: boolean;
  onClick: () => void;
  hasNewMessage?: boolean;
}

export default function ChatBotIcon({
  isOpen,
  onClick,
  hasNewMessage = false,
}: ChatBotIconProps) {
  return (
    <motion.button
      onClick={onClick}
      className="fixed bottom-6 right-6 w-16 h-16 rounded-full bg-linear-to-br from-yellow-600 to-amber-600 shadow-lg flex items-center justify-center z-50 hover:shadow-xl transition-shadow"
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      transition={{
        type: "spring",
        stiffness: 260,
        damping: 20,
      }}
    >
      {hasNewMessage && (
        <motion.span
          className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 500, damping: 15 }}
        />
      )}

      <motion.div
        animate={{ rotate: isOpen ? 90 : 0 }}
        transition={{ duration: 0.3 }}
      >
        {isOpen ? (
          <X className="w-7 h-7 text-white" />
        ) : (
          <MessageCircle className="w-7 h-7 text-white" />
        )}
      </motion.div>

      {/* Pulse animation for new messages */}
      {hasNewMessage && (
        <motion.span
          className="absolute inset-0 rounded-full bg-purple-400 opacity-30"
          animate={{ scale: [1, 1.5, 2], opacity: [0.3, 0.1, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        />
      )}
    </motion.button>
  );
}

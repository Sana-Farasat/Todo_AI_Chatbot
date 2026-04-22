"use client";
import { motion } from "framer-motion";
import { Pencil, Trash2, CheckCircle } from "lucide-react";

export interface Task {
  id: string;     // UUID (IMPORTANT: string, not number)
  title: string;
  description?: string;
  completed: boolean;
  created_at?: string;
  updated_at?: string;
}
interface TaskCardProps {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
  onEdit: () => void;
}

export default function TaskCard({
  task,
  onToggle,
  onDelete,
  onEdit,
}: TaskCardProps) {
  return (
    <motion.li
      layout
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="bg-gray-800 p-5 rounded-xl shadow-md flex justify-between items-start"
    >
      <div className="flex-1">
        <h3
          className={`text-lg font-semibold ${
            task.completed ? "line-through text-gray-400" : "text-white"
          }`}
        >
          {task.title}
        </h3>

        {task.description && (
          <p className="text-sm text-gray-400 mt-1">{task.description}</p>
        )}

        <span
          className={`text-xs mt-2 inline-block ${
            task.completed ? "text-green-400" : "text-yellow-400"
          }`}
        >
          {task.completed ? "Completed" : "Pending"}
        </span>
      </div>

      <div className="flex gap-3 ml-4">
        {/* Toggle Complete */}
        <button
          onClick={onToggle}
          className="text-green-400 hover:text-green-500"
          title="Mark Complete"
        >
          <CheckCircle size={20} />
        </button>

        {/* Edit */}
        <button
          onClick={onEdit}
          className="text-blue-400 hover:text-blue-500"
          title="Edit Task"
        >
          <Pencil size={20} />
        </button>

        {/* Delete */}
        <button
          onClick={onDelete}
          className="text-red-400 hover:text-red-500"
          title="Delete Task"
        >
          <Trash2 size={20} />
        </button>
      </div>
    </motion.li>
  );
}
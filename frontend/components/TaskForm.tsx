"use client";
import { useEffect, useState } from "react";

export interface Task {
  id: string;              // UUID (IMPORTANT: string, not number)
  title: string;
  description?: string;
  completed: boolean;
  created_at?: string;
  updated_at?: string;
}
interface TaskFormProps {
  onSubmit: (data: {
    title: string;
    description?: string;
  }) => void;
  defaultValues?: Task | null;
}

export default function TaskForm({
  onSubmit,
  defaultValues,
}: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (defaultValues) {
      setTitle(defaultValues.title);
      setDescription(defaultValues.description || "");
    }
  }, [defaultValues]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!title.trim()) return;

    onSubmit({
      title: title.trim(),
      description: description.trim(),
    });

    // Reset form after submit
    setTitle("");
    setDescription("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-gray-900 p-6 rounded-xl shadow-lg space-y-4"
    >
      <h3 className="text-lg font-semibold text-amber-400">
        {defaultValues ? "Edit Task" : "Add New Task"}
      </h3>

      <input
        type="text"
        placeholder="Task Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="w-full p-3 rounded-lg bg-gray-800 text-white outline-none focus:ring-2 focus:ring-amber-500"
      />

      <textarea
        placeholder="Task Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        className="w-full p-3 rounded-lg bg-gray-800 text-white outline-none focus:ring-2 focus:ring-amber-500"
        rows={3}
      />

      <button
        type="submit"
        className="bg-amber-500 hover:bg-amber-600 text-black font-semibold px-5 py-2 rounded-lg transition"
      >
        {defaultValues ? "Update Task" : "Save Task"}
      </button>
    </form>
  );
}
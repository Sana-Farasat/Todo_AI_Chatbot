"use client";
import { useState, useEffect, useId } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useApi from "@/lib/api";
import { authClient } from "@/lib/auth";
import TaskCard from "@/components/TaskCard";
import TaskForm from "@/components/TaskForm";
import Sidebar from "@/components/SideBar";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { toast } from "sonner";
import router from "next/router";
import Link from "next/link";

export default function Dashboard() {
  const api = useApi();
  const { data: session, isPending } = authClient.useSession(); // Better Auth session
  const userId = session?.user.id || "";

  const [tasks, setTasks] = useState<any[]>([]);
  const [editingTask, setEditingTask] = useState<any>(null);

  // Fetch tasks when userId is ready
  useEffect(() => {
    if (userId) fetchTasks();
  }, [userId]);

  async function fetchTasks() {
    try {
      const data = await api.getTasks(userId);
      setTasks(data);
    } catch (err) {
      console.error(err);
      toast.error("Failed to load tasks");
    }
  }

  async function handleSubmit(data: any) {
    try {
      if (editingTask) {
        await api.updateTask(userId, editingTask.id, data);
        setEditingTask(null);
      } else {
        await api.addTask(userId, data);
      }
      fetchTasks();
      toast.success("Task saved!");
    } catch (err) {
      console.error(err);
      toast.error("Error saving task");
    }
  }

  async function toggleComplete(taskId: number, completed: boolean) {
    try {
      await api.toggleComplete(userId, taskId, !completed);
      fetchTasks();
    } catch (err) {
      console.error(err);
      toast.error("Error updating status");
    }
  }

  async function deleteTask(taskId: number) {
    if (!confirm("Delete task?")) return;

    try {
      await api.deleteTask(userId, taskId);
      fetchTasks();
      toast.success("Task deleted");
    } catch (err) {
      console.error(err);
      toast.error("Error deleting task");
    }
  }

  if (isPending) return;

  <div className="flex justify-center items-center py-20 font-bold">
    <p className=" text-amber-500">Loading...</p>;
  </div>;
  // <p className="flex justify-center items-center text-amber-500">Loading...</p>;

  if (!session) return;

  <div className="flex justify-center items-center py-20 font-bold">
    <p>Not authenticated</p>;
  </div>;
  // <p>Not authenticated</p>;

  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <Header />
        <main className="p-8 flex-1 overflow-auto">
          <h2 className="text-2xl font-bold mb-6 text-amber-500">Tasks</h2>

          <TaskForm onSubmit={handleSubmit} defaultValues={editingTask} />

          <AnimatePresence>
            <motion.ul layout className="space-y-4 mt-6">
              {tasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onToggle={() => toggleComplete(task.id, task.completed)}
                  onDelete={() => deleteTask(task.id)}
                  onEdit={() => setEditingTask(task)}
                />
              ))}
            </motion.ul>
          </AnimatePresence>
        </main>
        <Footer />
      </div>
    </div>
  );
}

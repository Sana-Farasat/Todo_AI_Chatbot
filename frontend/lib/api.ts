"use client";
import { getJwtToken } from "@/lib/auth";

export default function useApi() {
  async function getToken(): Promise<string> {
    const token = await getJwtToken();
    if (!token) {
      throw new Error("Not authenticated - no token");
    }
    return token;
  }

  async function request(method: string, path: string, body?: any) {
    const token = await getToken();

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(errorText || "API request failed");
    }

    return res.json();
  }

  return {
    //getTasks: (userId: string) => request("GET", `/api/${userId}/tasks`),
    getTasks: (userId: string) => request("GET", `/api/tasks/${userId}`),
addTask: (userId: string, data: any) =>
       request("POST", `/api/tasks/${userId}`, data),
      
       updateTask: (userId: string, taskId: number, data: any) =>
         request("PUT", `/api/tasks/${userId}/${taskId}`, data),
      
       toggleComplete: (userId: string, taskId: number, completed: boolean) =>
      request("PATCH", `/api/tasks/${userId}/${taskId}/complete`, { completed }),
      
      deleteTask: (userId: string, taskId: number) =>
        request("DELETE", `/api/tasks/${userId}/${taskId}`),



    // addTask: (userId: string, data: any) =>
    //   request("POST", `/api/${userId}/tasks`, data),
    // updateTask: (userId: string, taskId: number, data: any) =>
    //   request("PUT", `/api/${userId}/tasks/${taskId}`, data),
    // toggleComplete: (userId: string, taskId: number, completed: boolean) =>
    //   request("PATCH", `/api/${userId}/tasks/${taskId}/complete`, {
    //     completed,
    //   }),
    // deleteTask: (userId: string, taskId: number) =>
    //   request("DELETE", `/api/${userId}/tasks/${taskId}`),

    // Chat endpoints
    // chat: (userId: string, message: string, conversationId?: number) =>
    //   request("POST", `/api/${userId}/chat`, { message, conversation_id: conversationId }),
    chat: (message: string, conversationId?: number) =>
  request("POST", `/api/chat`, { message, conversation_id: conversationId }),
    // getChatHistory: (userId: string, conversationId?: number) => {
    //   const path = conversationId 
    //     ? `/api/${userId}/chat/history?conversation_id=${conversationId}`
    //     : `/api/${userId}/chat/history`;
    //   return request("GET", path);
    // },

    getChatHistory: (conversationId?: number) => {
const path = conversationId
  ? `/api/chat/history?conversation_id=${conversationId}`
  : `/api/chat/history`;
  return request("GET", path);
    },
    // deleteConversation: (userId: string, conversationId: number) =>
    //   request("DELETE", `/api/${userId}/chat/conversation/${conversationId}`),
    deleteConversation: (conversationId: number) =>
  request("DELETE", `/api/chat/conversation/${conversationId}`)
  };
}

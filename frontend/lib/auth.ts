"use client";
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: "https://todo-ai-chatbot-arsx.vercel.app",
  plugins: [jwtClient()],
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
  updateUser,
  getSession,
  listSessions
} = authClient;

// JWT token get karne ka dedicated function
export async function getJwtToken(): Promise<string | null> {
  try {
    // JWT plugin se token lo using the correct API
    const { data, error } = await authClient.token();

    if (error || !data?.token) {
      return null;
    }

    return data.token;
  } catch {
    return null;
  }
}

// useAuth hook for user session
export function useAuth() {
  const { data: session, isPending } = useSession();
  
  return {
    user: session?.user?.email || session?.user?.id,
    session,
    isLoading: isPending,
    isAuthenticated: !!session,
  };
}

"use client";
import { Button } from "@/components/ui/button";
import { signOut } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function Header() {
  
  const router = useRouter();

  return (

    <header className="bg-gray-900 p-4 border-b border-gray-800 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-amber-500">Todo Dashboard</h1>
      <Button
        onClick={async () => {
          await signOut();
          router.push("/sign-in"); 
        }}
        variant="outline"
        className="border-amber-500 text-amber-500 hover:bg-amber-500 hover:text-black"
      >
        Logout
      </Button>
    </header>
  );
}

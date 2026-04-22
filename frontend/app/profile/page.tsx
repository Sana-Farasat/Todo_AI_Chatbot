"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { updateUser } from "@/lib/auth";
import Sidebar from "@/components/SideBar";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useSession } from "@/lib/auth";

const schema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  password: z.string().min(8).optional(),
});

export default function Profile() {
  const { data: session } = useSession();
  const { register, handleSubmit } = useForm({
    resolver: zodResolver(schema),
    defaultValues: { name: session?.user.name, email: session?.user.email },
  });

  const onSubmit = async (data: any) => {
    try {
      await updateUser(data);
      toast.success("Profile updated");
    } catch (err) {
      toast.error("Update failed");
    }
  };

  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <Header />
        <main className="p-8 flex-1">
          <h2 className="text-2xl font-bold mb-6 text-amber-500">Update Profile</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-md">
            <Input placeholder="Name" {...register("name")} className="border-gray-700 focus:border-amber-500" />
            <Input placeholder="Email" {...register("email")} className="border-gray-700 focus:border-amber-500" />
            <Input type="password" placeholder="New Password (optional)" {...register("password")} className="border-gray-700 focus:border-amber-500" />
            <Button type="submit" className="bg-amber-500 hover:bg-amber-600 text-black">Update</Button>
          </form>
        </main>
        <Footer />
      </div>
    </div>
  );
}
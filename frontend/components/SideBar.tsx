"use client";
import { Separator } from "@/components/ui/separator";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, User, Settings } from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/profile", label: "Profile", icon: User },
    { href: "/settings", label: "Settings", icon: Settings },
  ];

  return (
    <div className="w-64 bg-gray-900 h-screen p-6 fixed left-0 top-0 border-r border-gray-800 flex flex-col">
      <h2 className="text-xl font-bold mb-8 text-amber-500">Todo App</h2>
      <nav className="space-y-2 flex-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${
                isActive
                  ? "bg-amber-500 text-black font-semibold"
                  : "text-gray-300 hover:text-amber-500 hover:bg-gray-800"
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
      <Separator className="my-6 bg-gray-800" />
      <p className="text-xs text-gray-500 text-center">User Options</p>
    </div>
  );
}
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth"; 
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { motion } from "framer-motion";
import Link from "next/link";

export default function LoginPage() {
	const router = useRouter();
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [loading, setLoading] = useState(false);

	const handleLogin = async (e: React.FormEvent) => {
		e.preventDefault();
		setLoading(true);

		try {
     
			await authClient.signIn.email({
				email,
				password
			});

			toast.success("Login successful! Redirecting...");
			router.push("/dashboard");
		} catch (err: any) {
			toast.error(err.message || "Invalid credentials");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-linear-to-br from-gray-950 via-gray-900 to-black p-4">
			<motion.div
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 0.6, ease: "easeOut" }}
				className="w-full max-w-md space-y-8 bg-gray-900/80 backdrop-blur-xl p-8 rounded-2xl border border-gray-800 shadow-2xl shadow-amber-900/20"
			>
				<div className="text-center">
					<motion.h1
						initial={{ scale: 0.95 }}
						animate={{ scale: 1 }}
						className="text-4xl font-bold bg-linear-to-r from-amber-500 to-amber-300 bg-clip-text text-transparent"
					>
						Welcome Back
					</motion.h1>
					<p className="mt-3 text-gray-400">
						Login to manage your tasks
					</p>
				</div>

				<form onSubmit={handleLogin} className="mt-8 space-y-6">
					<div className="space-y-5">
						<div className="space-y-2">
							<Label htmlFor="email" className="text-gray-300">
								Email
							</Label>
							<Input
								id="email"
								type="email"
								placeholder="you@example.com"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
								required
								autoFocus
								className="bg-gray-800 border-gray-700 focus:border-amber-500 focus:ring-amber-500/30 text-white placeholder-gray-500"
							/>
						</div>

						<div className="space-y-2">
							<div className="flex items-center justify-between">
								<Label htmlFor="password" className="text-gray-300">
									Password
								</Label>
								<Link
									href="/forgot-password"
									className="text-sm text-amber-500 hover:text-amber-400 hover:underline"
								>
									Forgot password?
								</Link>
							</div>
							<Input
								id="password"
								type="password"
								placeholder="••••••••"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
								required
								className="bg-gray-800 border-gray-700 focus:border-amber-500 focus:ring-amber-500/30 text-white placeholder-gray-500"
							/>
						</div>
					</div>

					<Button
						type="submit"
						disabled={loading}
						className="w-full bg-linear-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-black font-medium py-6 text-lg transition-all duration-300 disabled:opacity-50"
					>
						{loading ? (
							<span className="flex items-center justify-center gap-2">
								<svg
									className="animate-spin h-5 w-5 text-black"
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
								>
									<circle
										className="opacity-25"
										cx="12"
										cy="12"
										r="10"
										stroke="currentColor"
										strokeWidth="4"
									/>
									<path
										className="opacity-75"
										fill="currentColor"
										d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
									/>
								</svg>
								Signing in...
							</span>
						) : (
							"Sign In"
						)}
					</Button>

					<div className="text-center text-sm text-gray-400">
						Don't have an account?{" "}
						<Link
							href="/sign-up"
							className="text-amber-500 hover:text-amber-400 font-medium hover:underline"
						>
							Sign up
						</Link>
					</div>
				</form>
			</motion.div>
		</div>
	);
}
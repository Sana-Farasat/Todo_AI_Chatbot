"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth"; // Fixed import
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { motion } from "framer-motion";
import Link from "next/link";

export default function SignupPage() {
	const router = useRouter();
	const [name, setName] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [loading, setLoading] = useState(false);

	const handleSignup = async (e: React.FormEvent) => {
		e.preventDefault();
		setLoading(true);

		try {
      
			await authClient.signUp.email({
				name,
				email,
				password
			});

			toast.success("Account created! Redirecting to login...");
			router.push("/sign-in");
		} catch (err: any) {
			console.error(err);
			toast.error(err.message || "Signup failed");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-linear-to-br from-gray-950 via-gray-900 to-black p-4">
			<motion.div
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 0.6 }}
				className="w-full max-w-md space-y-8 bg-gray-900/80 backdrop-blur-xl p-8 rounded-2xl border border-gray-800 shadow-2xl shadow-amber-900/20"
			>
				<div className="text-center">
					<h1 className="text-4xl font-bold bg-linear-to-r from-amber-500 to-amber-300 bg-clip-text text-transparent">
						Create Account
					</h1>
					<p className="mt-3 text-gray-400">
						Sign up to start managing your todos
					</p>
				</div>

				<form onSubmit={handleSignup} className="mt-8 space-y-6">
					<div className="space-y-5">
						<div className="space-y-2">
							<Label htmlFor="name" className="text-gray-300">
								Full Name
							</Label>
							<Input
								id="name"
								type="text"
								placeholder="Sana Khan"
								value={name}
								onChange={(e) => setName(e.target.value)}
								required
								className="bg-gray-800 border-gray-700 focus:border-amber-500 text-white"
							/>
						</div>

						<div className="space-y-2">
							<Label htmlFor="email" className="text-gray-300">
								Email
							</Label>
							<Input
								id="email"
								type="email"
								placeholder="sana@example.com"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
								required
								className="bg-gray-800 border-gray-700 focus:border-amber-500 text-white"
							/>
						</div>

						<div className="space-y-2">
							<Label htmlFor="password" className="text-gray-300">
								Password
							</Label>
							<Input
								id="password"
								type="password"
								placeholder="••••••••"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
								required
								className="bg-gray-800 border-gray-700 focus:border-amber-500 text-white"
							/>
						</div>
					</div>

					<Button
						type="submit"
						disabled={loading}
						className="w-full bg-linear-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-black font-medium py-6 text-lg disabled:opacity-50"
					>
						{loading ? "Creating account..." : "Sign Up"}
					</Button>

					<div className="text-center text-sm text-gray-400">
						Already have an account?{" "}
						<Link href="/sign-in" className="text-amber-500 hover:underline">
							Sign in
						</Link>
					</div>
				</form>
			</motion.div>
		</div>
	);
}
"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import { Bot, PlusCircle, Zap, Sparkles } from "lucide-react";

const features = [
	{
		icon: PlusCircle,
		title: "Manual Task Entry",
		description: "Add tasks with custom fields, priorities, due dates, and categories effortlessly",
		highlight: "Full control over task details",
	},
	{
		icon: Bot,
		title: "AI Chatbot Assistant",
		description: "Describe your tasks in plain language and let AI organize everything for you",
		highlight: "Natural conversation interface",
	},
	{
		icon: Zap,
		title: "NLP Processing",
		description: "Intelligent text understanding that extracts dates, priorities, and context automatically",
		highlight: "Smart parsing engine",
	},
];

export default function Home() {
	return (
		<div className="min-h-screen flex items-center justify-center bg-linear-to-br from-gray-950 via-gray-900 to-black p-4 py-12">
			<div className="w-full max-w-5xl space-y-16">
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.6, ease: "easeOut" }}
					className="text-center space-y-6"
				>
					<motion.h1
						initial={{ scale: 0.95, opacity: 0 }}
						animate={{ scale: 1, opacity: 1 }}
						transition={{ delay: 0.2, duration: 0.5 }}
						className="text-5xl md:text-6xl py-4 font-bold bg-linear-to-r from-amber-500 to-amber-300 bg-clip-text text-transparent"
					>
						Task Management System
					</motion.h1>

					<motion.p
						initial={{ opacity: 0 }}
						animate={{ opacity: 1 }}
						transition={{ delay: 0.4, duration: 0.5 }}
						className="text-xl text-gray-400 max-w-2xl mx-auto"
					>
						Manage your tasks three ways — manually, via chatbot, or with AI-powered NLP
					</motion.p>

					<motion.div
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ delay: 0.6, duration: 0.5 }}
						className="flex flex-col sm:flex-row gap-4 justify-center pt-4"
					>
						<Link
							href="/sign-in"
							className="px-10 py-4 bg-linear-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-black font-semibold text-lg rounded-xl transition-all duration-300 shadow-lg shadow-amber-900/30 hover:shadow-amber-800/50"
						>
							Login
						</Link>

						<Link
							href="/sign-up"
							className="px-10 py-4 bg-transparent border-2 border-amber-500 text-amber-500 hover:bg-amber-500/10 font-semibold text-lg rounded-xl transition-all duration-300 hover:border-amber-400 hover:text-amber-400"
						>
							Sign Up
						</Link>
					</motion.div>
				</motion.div>

				<motion.div
					initial={{ opacity: 0, y: 30 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 0.8, duration: 0.6 }}
					className="grid grid-cols-1 md:grid-cols-3 gap-6"
				>
					{features.map((feature, index) => (
						<motion.div
							key={feature.title}
							initial={{ opacity: 0, y: 20 }}
							animate={{ opacity: 1, y: 0 }}
							transition={{ delay: 1 + index * 0.15, duration: 0.5 }}
							className="group relative bg-gray-900/60 backdrop-blur-xl p-8 rounded-2xl border border-gray-800 hover:border-amber-500/50 transition-all duration-500 shadow-xl shadow-black/20 hover:shadow-amber-900/10"
						>
							<div className="absolute inset-0 bg-linear-to-br from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-500" />

							<div className="relative z-10">
								<div className="w-14 h-14 rounded-xl bg-linear-to-br from-amber-500/20 to-amber-600/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
									<feature.icon className="w-7 h-7 text-amber-500" />
								</div>

								<div className="flex items-center gap-2 mb-3">
									<Sparkles className="w-4 h-4 text-amber-400/70" />
									<span className="text-sm text-amber-400/70 font-medium tracking-wide uppercase">
										{feature.highlight}
									</span>
								</div>

								<h3 className="text-2xl font-bold text-white mb-3 group-hover:text-amber-100 transition-colors duration-300">
									{feature.title}
								</h3>

								<p className="text-gray-400 leading-relaxed group-hover:text-gray-300 transition-colors duration-300">
									{feature.description}
								</p>
							</div>
						</motion.div>
					))}
				</motion.div>

				<motion.div
					initial={{ opacity: 0 }}
					animate={{ opacity: 1 }}
					transition={{ delay: 1.5, duration: 0.6 }}
					className="text-center"
				>
					<p className="text-gray-500 text-sm">
						Choose your preferred way to add tasks — all powered by AI
					</p>
				</motion.div>
			</div>
		</div>
	);
}
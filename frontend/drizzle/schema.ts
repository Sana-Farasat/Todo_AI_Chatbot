// import { pgTable, text, timestamp, boolean } from "drizzle-orm/pg-core";

// // USER TABLE
// export const user = pgTable("user", {
// 	id: text("id").primaryKey(),
// 	name: text("name").notNull(), // Required field
// 	email: text("email").notNull().unique(), // Required field
// 	emailVerified: boolean("email_verified").notNull().default(false), // Required field
// 	image: text("image"), // Optional field
// 	createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
// 	updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
// });

// // SESSION TABLE
// export const session = pgTable("session", {
// 	id: text("id").primaryKey(),
// 	userId: text("user_id")
// 		.notNull()
// 		.references(() => user.id, { onDelete: "cascade" }),
// 	token: text("token").notNull().unique(), // Must be unique
// 	expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
// 	ipAddress: text("ip_address"), // Optional field
// 	userAgent: text("user_agent"), // Optional field
// 	createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
// 	updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
// });

// // ACCOUNT TABLE
// export const account = pgTable("account", {
// 	id: text("id").primaryKey(),
// 	userId: text("user_id")
// 		.notNull()
// 		.references(() => user.id, { onDelete: "cascade" }),
// 	accountId: text("account_id").notNull(),
// 	providerId: text("provider_id").notNull(),
// 	accessToken: text("access_token"), // Optional field
// 	refreshToken: text("refresh_token"), // Optional field
// 	accessTokenExpiresAt: timestamp("access_token_expires_at", { withTimezone: true }), // Optional field
// 	refreshTokenExpiresAt: timestamp("refresh_token_expires_at", { withTimezone: true }), // Optional field
// 	scope: text("scope"), // Optional field
// 	idToken: text("id_token"), // Optional field
// 	password: text("password"), // Optional field
// 	createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
// 	updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
// });

// // VERIFICATION TABLE
// export const verification = pgTable("verification", {
// 	id: text("id").primaryKey(),
// 	identifier: text("identifier").notNull(),
// 	value: text("value").notNull(),
// 	expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
// 	createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
// 	updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
// });

// // YOUR CUSTOM TASK TABLE (not part of Better Auth core schema)
// export const task = pgTable("task", {
// 	id: text("id").primaryKey(),
// 	userId: text("user_id")
// 		.notNull()
// 		.references(() => user.id, { onDelete: "cascade" }),
// 	title: text("title").notNull(),
// 	description: text("description"),
// 	status: text("status").notNull().default("pending"),
// 	priority: text("priority").notNull().default("medium"),
// 	dueDate: timestamp("due_date", { withTimezone: true }),
// 	completedAt: timestamp("completed_at", { withTimezone: true }),
// 	createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
// 	updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
// });

// // JWKS TABLE (required for JWT plugin)
// export const jwks = pgTable("jwks", {
// 	id: text("id").primaryKey(),
// 	publicKey: text("public_key").notNull(),
// 	privateKey: text("private_key").notNull(),
// 	createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
// });

/////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

import { pgTable, text, timestamp, boolean } from "drizzle-orm/pg-core";

/* =========================
   USER TABLE (Better Auth)
========================= */

export const user = pgTable("user", {
  id: text("id").primaryKey(),

  name: text("name").notNull(),

  email: text("email").notNull().unique(),

  emailVerified: boolean("email_verified")
    .notNull()
    .default(false),

  image: text("image"),

  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .defaultNow(),

  updatedAt: timestamp("updated_at", { withTimezone: true })
    .notNull()
    .defaultNow(),
});


/* =========================
   SESSION TABLE
========================= */

export const session = pgTable("session", {
  id: text("id").primaryKey(),

  userId: text("user_id")
    .notNull()
    .references(() => user.id, { onDelete: "cascade" }),

  token: text("token").notNull().unique(),

  expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),

  ipAddress: text("ip_address"),

  userAgent: text("user_agent"),

  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .defaultNow(),

  updatedAt: timestamp("updated_at", { withTimezone: true })
    .notNull()
    .defaultNow(),
});


/* =========================
   ACCOUNT TABLE (OAuth etc)
========================= */

export const account = pgTable("account", {
  id: text("id").primaryKey(),

  userId: text("user_id")
    .notNull()
    .references(() => user.id, { onDelete: "cascade" }),

  accountId: text("account_id").notNull(),

  providerId: text("provider_id").notNull(),

  accessToken: text("access_token"),

  refreshToken: text("refresh_token"),

  accessTokenExpiresAt: timestamp("access_token_expires_at", {
    withTimezone: true,
  }),

  refreshTokenExpiresAt: timestamp("refresh_token_expires_at", {
    withTimezone: true,
  }),

  scope: text("scope"),

  idToken: text("id_token"),

  password: text("password"),

  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .defaultNow(),

  updatedAt: timestamp("updated_at", { withTimezone: true })
    .notNull()
    .defaultNow(),
});


/* =========================
   VERIFICATION TABLE
========================= */

export const verification = pgTable("verification", {
  id: text("id").primaryKey(),

  identifier: text("identifier").notNull(),

  value: text("value").notNull(),

  expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),

  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .defaultNow(),

  updatedAt: timestamp("updated_at", { withTimezone: true })
    .notNull()
    .defaultNow(),
});


/* =========================
   JWKS TABLE (JWT Plugin)
========================= */

export const jwks = pgTable("jwks", {
  id: text("id").primaryKey(),

  publicKey: text("public_key").notNull(),

  privateKey: text("private_key").notNull(),

  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .defaultNow(),
});


/* =========================
   TASK TABLE (Your App)
========================= */

export const task = pgTable("tasks", {
  id: text("id").primaryKey(),

  userId: text("user_id")
    .notNull()
    .references(() => user.id, { onDelete: "cascade" }),

  title: text("title").notNull(),

  description: text("description"),

  status: text("status")
    .notNull()
    .default("pending"), // pending | completed

  priority: text("priority")
    .notNull()
    .default("medium"), // low | medium | high

  dueDate: timestamp("due_date", { withTimezone: true }),

  //completedAt: timestamp("completed_at", { withTimezone: true }),
 completed: boolean("completed")
    .notNull()
    .default(false),

  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .defaultNow(),

  updatedAt: timestamp("updated_at", { withTimezone: true })
    .notNull()
    .defaultNow(),
});
import type { Config } from "drizzle-kit";

export default {
  schema: "./drizzle/schema.ts",
  out: "./drizzle/migrations",
  dialect: "postgresql",
//   dbCredentials: {
//     url: process.env.DATABASE_URL!,
//   },
dbCredentials: {
    url: "postgresql://neondb_owner:npg_Jy5GuY7nbDTA@ep-wispy-shape-aigc2d0u-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

},
  verbose: true,
} satisfies Config;
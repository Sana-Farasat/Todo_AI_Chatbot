Skill: Next.js 16 App Router + Better Auth + Authenticated API calls

Must use:
- App Router (app/ directory)
- Server Components by default
- lib/api.ts → fetch with credentials + Authorization header
- Better Auth v0.5+ with JWT plugin enabled
- Tailwind + shadcn/ui recommended

API client example (lib/api.ts):
const api = {
  async getTasks(userId) {
    const token = await getToken(); // from better-auth
    return fetch(`/api/${userId}/tasks`, {
      headers: { Authorization: `Bearer ${token}` }
    });
  }
}
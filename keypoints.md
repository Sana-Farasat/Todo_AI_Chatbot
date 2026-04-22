# Key Points

1. Used Better Auth Library for authentication and Its our choice k authentication control backend k pass rkhen ya frontend..
2. Is project m control frontend k pass hai..
3. Control jb backend k pass hoga tw login and signup dono orutes bnengy lekin jb frontend k pass control hoga tw better auth library kch login and signup k routes nextjs m internally create krdeta hai..
4. Control pass hona means DB schema forntend m hai then forntend cli se migrations command run ki..
5. - npx drizzle-kit generate
6. - npx drizzle-kit push
7. ORM (Object Relational Mapper) hmne drizzle use kiya hai..

---

## Drizzle ORM (Detailed Notes)

**Drizzle (usually called Drizzle ORM) ek modern TypeScript/JavaScript ORM (Object Relational Mapper) hai jo databases (PostgreSQL, MySQL, SQLite, etc.) ke saath kaam karne ke liye use hota hai.**

Simple words mein:
- Ye aapko SQL likhne ki jagah TypeScript code se database manage karne deta hai.

### Drizzle kya karta hai?

Drizzle ORM aapko help karta hai:
- Database tables define karne mein (TypeScript se)
- Queries likhne mein (SELECT, INSERT, UPDATE, DELETE)
- Migrations manage karne mein
- Type-safe database operations karne mein (TypeScript safety)

### drizzle-kit kya hai?

drizzle-kit ek CLI tool hai jo Drizzle ORM ke saath use hota hai.
Ye mainly 2 kaam karta hai:

1. **npx drizzle-kit generate**
   - Ye command migration files generate karti hai.
   - Matlab: Aap apni schema file change karte ho, Ye tool us change ka SQL migration bana deta hai.
   - Example: `npx drizzle-kit generate` ➡️ Output: migrations/ folder mein SQL files

2. **npx drizzle-kit push**
   - Ye command direct database ko update karti hai based on your schema.
   - Matlab: Jo schema aapne likha hai, Usko directly database pe apply kar deta hai.
   - Example: `npx drizzle-kit push`
   - Note: Ye migrations file banaye bina direct DB update kar sakta hai. Development mein useful, but production mein careful use hota hai.

### Difference simple way mein:

| Command | Kaam |
|---------|-----|
| generate | migration files banata hai (safe & structured way) |
| push | directly database update karta hai |

### Drizzle kyun use hota hai?

- TypeScript-first ORM
- Prisma se lighter & faster feel
- SQL jaisa control but JS/TS safety ke saath
- Better for modern backend (Next.js, Node.js apps)

### Ek line mein:

> Drizzle ek TypeScript ORM hai jo database ko code se manage karne deta hai, aur drizzle-kit uska migration/push tool hai.

### Drizzle ORM = abstraction layer (bridge) between your code and database

- Drizzle ek translator hai jo DB aur code ke beech hota hai.

---

## Database Info

- **URL:** https://console.neon.tech
- Create new project and copy connection string
- **DB Name for this project:** Todo_Chatbot_App

---

## App Requirements

1. Todo app should be like this that every use will manage multiple tasks in its own dashboard and every use will have its own dashboard..
2. Chatbot will use same Dashboard and Task Table too, No duplication..

---

## HTTP Error Codes

| Error Code | Meaning |
|-----------|---------|
| 405 | the server received the request but does not allow the PUT method for that route.405 Method Not Allowed.. |
| 403 | backend or frontedn kch mismatch horha hai.. |
| 404 | page hi n mila.. |
| 422 | kch miss horha hai.. |
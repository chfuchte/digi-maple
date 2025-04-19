import { Request } from "express";
import { db } from "../db";
import { sessions, users } from "../db/schema";
import { and, eq, sql } from "drizzle-orm";
import { tryCatch } from "./trycatch";

export async function auth(req: Request) {
    const token = req.cookies["token"];

    if (!token) return null;

    const result = await tryCatch(
        db
            .select({
                session: { id: sessions.id },
                user: {
                    id: users.id,
                    email: users.email,
                    full_name: users.full_name,
                },
            })
            .from(sessions)
            .innerJoin(users, eq(sessions.userId, users.id))
            .where(and(eq(sessions.token, token), sql`(strftime('%s', 'now') - ${sessions.createdAt}) < 172800`)), // 2 days in seconds
    );

    if (result.error || result.data.length === 0) return null;

    return result.data[0];
}

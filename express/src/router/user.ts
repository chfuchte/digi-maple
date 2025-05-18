import { Router } from "express";
import { auth } from "../utils/auth";
import { tryCatch } from "../utils/trycatch";
import { db } from "../db";
import { sessions, users } from "../db/schema";
import { eq } from "drizzle-orm";
import { randomBytes } from "node:crypto";
import z from "zod";
import getLogger from "../utils/logger";

export function userRouter() {
    const router = Router();
    const logger = getLogger("router.user");

    router.post("/api/auth/register", async (req, res) => {
        logger("INFO", "POST /api/auth/register called");

        const bodySchema = z.object({
            full_name: z.string(),
            email: z.string().email(),
            password: z.string(),
        });

        const body = bodySchema.safeParse(req.body);
        if (!body.success) {
            logger("WARN", `Validation failed: ${JSON.stringify(body.error.errors)}`);
            res.status(400).json({ error: body.error.errors });
            return;
        }

        const { full_name, email, password } = body.data;

        logger("DEBUG", `Checking if email already exists: ${email}`);
        const uniqueCheckResult = await tryCatch(db.select().from(users).where(eq(users.email, email)));

        if (uniqueCheckResult.error) {
            logger("ERROR", `DB error checking existing user: ${uniqueCheckResult.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }

        if (uniqueCheckResult.data.length > 0) {
            logger("INFO", `Email already registered: ${email}`);
            res.status(400).json({ error: "Email already registered" });
            return;
        }

        logger("DEBUG", `Inserting new user: ${email}`);
        const result = await tryCatch(db.insert(users).values({ email, full_name, password }));

        if (result.error) {
            logger("ERROR", `Error inserting new user: ${result.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }

        logger("INFO", `User created successfully: ${email}`);
        res.status(200).json({ message: "User created" });
    });

    router.post("/api/auth/login", async (req, res) => {
        logger("INFO", "POST /api/auth/login called");

        const bodySchema = z.object({
            email: z.string().email(),
            password: z.string(),
        });

        const body = bodySchema.safeParse(req.body);
        if (!body.success) {
            logger("WARN", `Validation failed: ${JSON.stringify(body.error.errors)}`);
            res.status(400).json({ error: body.error.errors });
            return;
        }

        const { email, password } = body.data;

        logger("DEBUG", `Attempting login for: ${email}`);
        const result = await tryCatch(db.select().from(users).where(eq(users.email, email)));

        if (result.error) {
            logger("ERROR", `DB error during login: ${result.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }

        const { data } = result;

        if (!data || data.length === 0) {
            logger("WARN", `Login failed: No user found for ${email}`);
            res.status(401).json({ error: "Invalid credentials" });
            return;
        }

        const user = data[0];
        const passwordMatch = password === user.password;

        if (!passwordMatch) {
            logger("WARN", `Login failed: Invalid password for ${email}`);
            res.status(401).json({ error: "Invalid credentials" });
            return;
        }

        const token = randomBytes(32).toString("hex");
        logger("DEBUG", `Generated session token for ${email}`);

        const session = await tryCatch(
            db.insert(sessions).values({
                userId: user.id,
                token,
            }),
        );

        if (session.error) {
            logger("ERROR", `Failed to create session: ${session.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }

        res.cookie("token", token, {
            httpOnly: true,
            secure: process.env.NODE_ENV === "production",
            maxAge: 1000 * 60 * 60 * 24 * 7,
        });

        logger("INFO", `User logged in: ${email}`);
        res.status(200).json({
            message: "Logged in",
        });
    });

    router.post("/api/auth/logout", async (req, res) => {
        logger("INFO", "POST /api/auth/logout called");

        const authRes = await auth(req);

        if (!authRes) {
            logger("WARN", "Logout failed: Unauthorized");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        const { session } = authRes;

        const result = await tryCatch(db.delete(sessions).where(eq(sessions.id, session.id)));

        if (result.error) {
            logger("ERROR", `Failed to delete session: ${result.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }

        logger("INFO", `User logged out, session ${session.id}`);
        res.clearCookie("token").status(200).json({ message: "Logged out" });
    });

    router.get("/api/auth/whoami", async (req, res) => {
        logger("INFO", "GET /api/auth/whoami called");

        const authRes = await auth(req);

        if (!authRes) {
            logger("WARN", "Whoami failed: Unauthorized");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        const { user } = authRes;
        logger("INFO", `Returning user info for: ${user.email}`);

        res.status(200).json({
            id: user.id,
            full_name: user.full_name,
            email: user.email,
        });
    });

    return router;
}

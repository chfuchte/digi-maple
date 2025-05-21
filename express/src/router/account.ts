import { Router } from "express";
import { auth } from "../utils/auth";
import { tryCatch } from "../utils/trycatch";
import { db } from "../db";
import z from "zod";
import getLogger from "../utils/logger";
import { users } from "../db/schema";
import { eq } from "drizzle-orm";

export function accountRouter() {
    const router = Router();
    const logger = getLogger("router.account");

    router.delete("/api/account", async (req, res) => {
        logger("INFO", "DELETE /api/account called");

        const authRes = await auth(req);

        if (!authRes) {
            logger("ERROR", "Authentication failed: Unauthorized");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        const bodySchema = z.object({
            password: z.string(),
        });
        const body = bodySchema.safeParse(req.body);
        if (!body.success) {
            logger("WARN", `Validation failed: ${JSON.stringify(body.error.errors)}`);
            res.status(400).json({ error: body.error.errors });
            return;
        }
        const { password } = body.data;
        const userId = authRes.user.id;
        const user = await tryCatch(db.select().from(users).where(eq(users.id, userId)));
        if (user.error) {
            logger("ERROR", `DB error fetching user: ${user.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }
        if (user.data.length === 0) {
            logger("ERROR", "User not found");
            res.status(404).json({ error: "User not found" });
            return;
        }
        const existingUser = user.data[0];
        if (existingUser.password !== password) {
            logger("WARN", "Account deletion failed: Incorrect password");
            res.status(401).json({ error: "Incorrect password" });
            return;
        }
        const result = await tryCatch(db.delete(users).where(eq(users.id, userId)));
        if (result.error) {
            logger("ERROR", `DB error deleting user: ${result.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }
        logger("INFO", `User deleted: ${userId}`);
        res.status(200).json({ message: "Account deleted" });
    });

    router.patch("/api/account/chpwd", async (req, res) => {
        logger("INFO", "PATCH /api/account/chpwd called");
        const authRes = await auth(req);
        if (!authRes) {
            logger("ERROR", "Authentication failed: Unauthorized");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }
        const userId = authRes.user.id;
        const bodySchema = z.object({
            old_password: z.string(),
            new_password: z.string(),
        });
        const body = bodySchema.safeParse(req.body);
        if (!body.success) {
            logger("WARN", `Validation failed: ${JSON.stringify(body.error.errors)}`);
            res.status(400).json({ error: body.error.errors });
            return;
        }
        const { old_password, new_password } = body.data;
        const user = await tryCatch(db.select().from(users).where(eq(users.id, userId)));
        if (user.error) {
            logger("ERROR", `DB error fetching user: ${user.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }
        if (user.data.length === 0) {
            logger("ERROR", "User not found");
            res.status(404).json({ error: "User not found" });
            return;
        }
        const existingUser = user.data[0];
        if (existingUser.password !== old_password) {
            logger("WARN", "Password change failed: Incorrect old password");
            res.status(401).json({ error: "Incorrect old password" });
            return;
        }
        const result = await tryCatch(db.update(users).set({ password: new_password }).where(eq(users.id, userId)));
        if (result.error) {
            logger("ERROR", `DB error updating password: ${result.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }
        logger("INFO", `Password changed for user: ${userId}`);
        res.status(200).json({ message: "Password changed" });
    });

    router.patch("/api/account/chemail", async (req, res) => {
        logger("INFO", "PATCH /api/account/chemail called");
        const authRes = await auth(req);
        if (!authRes) {
            logger("ERROR", "Authentication failed: Unauthorized");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }
        const userId = authRes.user.id;
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
        const user = await tryCatch(db.select().from(users).where(eq(users.id, userId)));
        if (user.error) {
            logger("ERROR", `DB error fetching user: ${user.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }
        if (user.data.length === 0) {
            logger("ERROR", "User not found");
            res.status(404).json({ error: "User not found" });
            return;
        }
        const existingUser = user.data[0];
        if (existingUser.password !== password) {
            logger("WARN", "Email change failed: Incorrect password");
            res.status(401).json({ error: "Incorrect password" });
            return;
        }
        const result = await tryCatch(db.update(users).set({ email }).where(eq(users.id, userId)));
        if (result.error) {
            logger("ERROR", `DB error updating email: ${result.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }
        logger("INFO", `Email changed for user: ${userId}`);
        res.status(200).json({ message: "Email changed" });
    });

    router.patch("/api/account/chname", async (req, res) => {
        logger("INFO", "PATCH /api/account/chname called");
        const authRes = await auth(req);
        if (!authRes) {
            logger("ERROR", "Authentication failed: Unauthorized");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }
        const userId = authRes.user.id;
        const bodySchema = z.object({
            full_name: z.string(),
        });
        const body = bodySchema.safeParse(req.body);
        if (!body.success) {
            logger("WARN", `Validation failed: ${JSON.stringify(body.error.errors)}`);
            res.status(400).json({ error: body.error.errors });
            return;
        }
        const { full_name } = body.data;
        const result = await tryCatch(db.update(users).set({ full_name }).where(eq(users.id, userId)));
        if (result.error) {
            logger("ERROR", `DB error updating name: ${result.error}`);
            res.status(500).json({ error: "Internal server error" });
            return;
        }
        logger("INFO", `Name changed for user: ${userId}`);
        res.status(200).json({ message: "Name changed" });
    });

    return router;
}

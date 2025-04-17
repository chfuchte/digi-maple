import { relations, sql } from "drizzle-orm";
import { sqliteTable, integer, text } from "drizzle-orm/sqlite-core";
import { sessions } from "./session";

export const users = sqliteTable("users", {
    id: integer("id").primaryKey(),
    email: text("email").notNull().unique(),
    full_name: text("full_name").notNull(),
    password: text("password").notNull(),
});

export const userRelations = relations(users, ({ many }) => ({
    sessions: many(sessions),
}));

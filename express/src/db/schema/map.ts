import { relations } from "drizzle-orm";
import { sqliteTable, integer, text } from "drizzle-orm/sqlite-core";
import { users } from "./user";

export const maps = sqliteTable("maps", {
    id: integer("id").primaryKey(),
    userId: integer("user_id")
        .notNull()
        .references(() => users.id, { onDelete: "cascade" }),
    name: text("name").notNull(),
    imgWidth: integer("img_w"),
    imgHeight: integer("img_h"),
});

export const mapRelations = relations(maps, ({ one, many }) => ({
    user: one(users, {
        fields: [maps.userId],
        references: [users.id],
    }),
    markers: many(markers),
}));

export const markers = sqliteTable("markers", {
    id: integer("id").primaryKey(),
    mapId: integer("map_id")
        .notNull()
        .references(() => maps.id, { onDelete: "cascade" }),
    x: integer("x").notNull(),
    y: integer("y").notNull(),
    title: text("title").notNull(),
    description: text("description").notNull(),
    icon: text("icon").notNull(),
    color: text("color").notNull(),
});

export const markerRelations = relations(markers, ({ one }) => ({
    map: one(maps, {
        fields: [markers.mapId],
        references: [maps.id],
    }),
}));

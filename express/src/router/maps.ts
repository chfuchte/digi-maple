import express, { Router } from "express";
import { auth } from "../utils/auth";
import multer from "multer";
import env from "../env";
import { extname } from "node:path";
import { mkdirSync } from "node:fs";
import { tryCatch } from "../utils/trycatch";
import { db } from "../db";
import { maps, markers } from "../db/schema";
import { and, eq, sql } from "drizzle-orm";
import sharp from "sharp";
import getLogger from "../utils/logger";
import { unlink } from "node:fs/promises";
import z from "zod";

const logger = getLogger("router.maps");

const storage = multer.diskStorage({
    destination: (_req, _file, cb) => {
        mkdirSync(env.ABSOLUTE_IMAGES_DIR, { recursive: true });
        cb(null, env.ABSOLUTE_IMAGES_DIR);
    },
    filename: (req, file, cb) => {
        const mapId = req.params.id;
        const ext = extname(file.originalname);
        cb(null, `${mapId}_original${ext}`);
    },
});

const upload = multer({
    storage,
    fileFilter: (_req, file, cb) => {
        const allowedTypes = ["image/webp", "image/jpeg", "image/jpg", "image/png"];
        if (allowedTypes.includes(file.mimetype)) {
            cb(null, true);
        } else {
            cb(new Error("Only .webp, .jpg, .jpeg, and .png formats are allowed"));
        }
    },
});

export function mapsRouter() {
    const router = Router();

    router.use("/api/maps/images", express.static(env.ABSOLUTE_IMAGES_DIR));
    logger("INFO", `Serving static files from ${env.ABSOLUTE_IMAGES_DIR} at /api/maps/images`);

    router.post("/api/maps/upload/:id", upload.single("image"), async (req, res) => {
        logger("INFO", `POST /api/maps/upload/${req.params.id} called`);

        const authRes = await auth(req);
        if (!authRes) {
            logger("WARN", "Unauthorized access attempt to map upload");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        if (Number.isNaN(req.params.id)) {
            logger("WARN", `Invalid map ID: ${req.params.id}`);
            res.status(400).json({ error: "Map id is required and needs to be an int" });
            return;
        }

        const mapId = parseInt(req.params.id);

        if (!req.file) {
            logger("WARN", `No file uploaded for map ID: ${mapId}`);
            res.status(400).json({ error: "Image file is required" });
            return;
        }

        const originalPath = req.file.path;
        const webpPath = `${env.ABSOLUTE_IMAGES_DIR}/${mapId}.webp`;

        const convertResult = await tryCatch(sharp(originalPath).webp({ quality: 90 }).toFile(webpPath));

        if (convertResult.error) {
            logger("ERROR", `Failed to convert image to webp for map ${mapId}: ${convertResult.error}`);
            res.status(500).json({ error: "Failed to convert image" });
            return;
        }

        const imageUrl = `http://localhost:8080/api/maps/images/${mapId}.webp`;

        logger("DEBUG", `File uploaded: ${req.file.originalname} -> ${webpPath}`);

        const metadataResult = await tryCatch(sharp(webpPath).metadata());

        if (metadataResult.error) {
            logger("ERROR", `Failed to read image metadata for map ${mapId}: ${metadataResult.error}`);
            res.status(500).json({ error: "Failed to read image metadata" });
            return;
        }

        const { width: imgWidth = 0, height: imgHeight = 0 } = metadataResult.data;
        logger("DEBUG", `Image dimensions for map ${mapId}: ${imgWidth}x${imgHeight}`);

        const result = await tryCatch(db.update(maps).set({ imgWidth, imgHeight }).where(eq(maps.id, mapId)));

        if (result.error) {
            logger("ERROR", `Failed to update map ${mapId}: ${result.error}`);
            res.status(500).json({ error: "Failed to update map" });
            return;
        }

        if (result.data.rowsAffected === 0) {
            logger("WARN", `Map not found with ID: ${mapId}`);
            res.status(404).json({ error: "Map not found" });
            return;
        }

        logger("INFO", `Map ${mapId} updated with new image: ${imageUrl}`);
        res.status(200).json({ imageUrl, imgWidth, imgHeight });

        const deleteResult = await tryCatch(unlink(originalPath));

        if (deleteResult.error) {
            logger("ERROR", `Failed to delete original image: ${deleteResult.error}`);
            return;
        }

        logger("DEBUG", `Original image deleted: ${originalPath}`);
    });

    router.post("/api/maps", async (req, res) => {
        logger("INFO", "POST /api/maps called");

        const authRes = await auth(req);
        if (!authRes) {
            logger("WARN", "Unauthorized access attempt to create map");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        const { name } = req.body;

        if (!name) {
            logger("WARN", "Name is required for creating a map");
            res.status(400).json({ error: "Name is required" });
            return;
        }

        const result = await tryCatch(db.insert(maps).values({ name, userId: authRes.user.id }));

        if (result.error) {
            logger("ERROR", `Failed to create map: ${result.error}`);
            res.status(500).json({ error: "Failed to create map" });
            return;
        }

        logger("INFO", `Map created with ID: ${result.data.lastInsertRowid}`);
        res.status(200).json({ id: Number(result.data.lastInsertRowid) });
    });

    router.get("/api/maps/my", async (req, res) => {
        logger("INFO", "GET /api/maps/my called");

        const authRes = await auth(req);
        if (!authRes) {
            logger("WARN", "Unauthorized access attempt to get user's maps");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        const userId = authRes.user.id;

        const result = await tryCatch(
            db
                .select({ id: maps.id, name: maps.name, imgWidth: maps.imgWidth, imgHeight: maps.imgHeight })
                .from(maps)
                .where(eq(maps.userId, userId)),
        );

        if (result.error) {
            logger("ERROR", `Failed to get user's maps: ${result.error}`);
            res.status(500).json({ error: "Failed to get user's maps" });
            return;
        }

        logger("INFO", `User's maps retrieved: ${result.data.length} maps found`);

        res.status(200).json(
            result.data.map((map) => ({
                id: map.id,
                name: map.name,
                imgUrl: `http://localhost:8080/api/maps/images/${map.id}.webp`,
                imgWidth: map.imgWidth ? map.imgWidth : undefined,
                imgHeight: map.imgHeight ? map.imgHeight : undefined,
            })),
        );
    });

    router.get("/api/maps/search", async (req, res) => {
        logger("INFO", "GET /api/maps/search called");

        const searchTerm = req.query.s as string;

        if (!searchTerm) {
            logger("WARN", "Search term is required for searching maps");
            res.status(400).json({ error: "Search term is required" });
            return;
        }

        const result = await tryCatch(
            db
                .select({ id: maps.id, name: maps.name, imgWidth: maps.imgWidth, imgHeight: maps.imgHeight })
                .from(maps)
                .where(sql`${maps.name} LIKE ${`%${searchTerm}%`}`),
        );

        if (result.error) {
            logger("ERROR", `Failed to search maps: ${result.error}`);
            res.status(500).json({ error: "Failed to search maps" });
            return;
        }

        if (result.data.length === 0) {
            logger("INFO", "No maps found matching the search term");
            res.status(404).json({ error: "No maps found" });
            return;
        }

        logger("INFO", `Maps found matching the search term: ${result.data.length} maps found`);

        res.status(200).json(
            result.data.map((map) => ({
                id: map.id,
                name: map.name,
                imgUrl: `/api/maps/images/${map.id}.webp`,
                imgWidth: map.imgWidth ? map.imgWidth : undefined,
                imgHeight: map.imgHeight ? map.imgHeight : undefined,
            })),
        );
    });

    router.get("/api/maps/:id", async (req, res) => {
        logger("INFO", `GET /api/maps/${req.params.id} called`);

        if (Number.isNaN(req.params.id)) {
            logger("WARN", `Invalid map ID: ${req.params.id}`);
            res.status(400).json({ error: "Map id is required and needs to be an int" });
            return;
        }

        const mapId = parseInt(req.params.id);

        const result = await tryCatch(
            db.query.maps.findFirst({
                with: {
                    markers: true,
                },
                where: eq(maps.id, mapId),
            }
            )
        );

        if (result.error) {
            logger("ERROR", `Failed to get map details: ${result.error}`);
            res.status(500).json({ error: "Failed to get map details" });
            return;
        }

        console.log(result.data);

        if (!result.data) {
            logger("WARN", `Map not found with ID: ${mapId}`);
            res.status(404).json({ error: "Map not found" });
            return;
        }

        logger("INFO", `Map details retrieved for ID: ${mapId}`);
        res.status(200).json({
            id: result.data.id,
            name: result.data.name,
            imgWidth: result.data.imgWidth ? result.data.imgWidth : undefined,
            imgHeight: result.data.imgHeight ? result.data.imgHeight : undefined,
            imgUrl: `http://localhost:8080/api/maps/images/${mapId}.webp`,
            markers: result.data.markers.map((marker) => ({
                id: marker.id,
                x: marker.x,
                y: marker.y,
                title: marker.title,
                description: marker.description,
                color: marker.color,
                icon: marker.icon,
            })),
        });
    });

    router.delete("/api/maps/:id", async (req, res) => {
        logger("INFO", `DELETE /api/maps/${req.params.id} called`);

        const authRes = await auth(req);
        if (!authRes) {
            logger("WARN", "Unauthorized access attempt to delete map");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        if (Number.isNaN(req.params.id)) {
            logger("WARN", `Invalid map ID: ${req.params.id}`);
            res.status(400).json({ error: "Map id is required and needs to be an int" });
            return;
        }

        const mapId = parseInt(req.params.id);

        const result = await tryCatch(db.delete(maps).where(eq(maps.id, mapId)));

        if (result.error) {
            logger("ERROR", `Failed to delete map: ${result.error}`);
            res.status(500).json({ error: "Failed to delete map" });
            return;
        }

        if (result.data.rowsAffected === 0) {
            logger("WARN", `Map not found with ID: ${mapId}`);
            res.status(404).json({ error: "Map not found" });
            return;
        }

        logger("INFO", `Map deleted with ID: ${mapId}`);
        res.status(200).json({ message: "Map deleted successfully" });
    });

    router.patch("/api/maps/:id", async (req, res) => {
        logger("INFO", `PATCH /api/maps/${req.params.id} called`);

        const authRes = await auth(req);
        if (!authRes) {
            logger("WARN", "Unauthorized access attempt to update map");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        if (Number.isNaN(req.params.id)) {
            logger("WARN", `Invalid map ID: ${req.params.id}`);
            res.status(400).json({ error: "Map id is required and needs to be an int" });
            return;
        }

        const mapId = parseInt(req.params.id);

        const body = z
            .object({
                name: z.string(),
            })
            .safeParse(req.body);
        if (!body.success) {
            logger("WARN", `Validation failed: ${JSON.stringify(body.error.errors)}`);
            res.status(400).json({ error: body.error.errors });
            return;
        }

        const { name } = body.data;

        const result = await tryCatch(db.update(maps).set({ name }).where(eq(maps.id, mapId)));

        if (result.error) {
            logger("ERROR", `Failed to update map: ${result.error}`);
            res.status(500).json({ error: "Failed to update map" });
            return;
        }

        if (result.data.rowsAffected === 0) {
            logger("WARN", `Map not found with ID: ${mapId}`);
            res.status(404).json({ error: "Map not found" });
            return;
        }

        logger("INFO", `Map updated with ID: ${mapId}`);
        res.status(200).json({ message: "Map updated successfully" });
    });

    router.post("/api/maps/:id/markers", async (req, res) => {
        logger("INFO", `POST /api/maps/${req.params.id}/markers called`);

        const authRes = await auth(req);
        if (!authRes) {
            logger("WARN", "Unauthorized access attempt to add marker to map");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        if (Number.isNaN(req.params.id)) {
            logger("WARN", `Invalid map ID: ${req.params.id}`);
            res.status(400).json({ error: "Map id is required and needs to be an int" });
            return;
        }

        const mapId = parseInt(req.params.id);

        // check if the map exists and belongs to the user
        const mapCheckResult = await tryCatch(
            db
                .select({ id: maps.id })
                .from(maps)
                .where(and(eq(maps.id, mapId), eq(maps.userId, authRes.user.id))),
        );

        if (mapCheckResult.error) {
            logger("ERROR", `Failed to check map existence: ${mapCheckResult.error}`);
            res.status(500).json({ error: "Failed to check map existence" });
            return;
        }

        const body = z
            .object({
                x: z.number(),
                y: z.number(),
                title: z.string(),
                description: z.string(),
                color: z.string(),
                icon: z.string(),
            })
            .safeParse(req.body);
        if (!body.success) {
            logger("WARN", `Validation failed: ${JSON.stringify(body.error.errors)}`);
            res.status(400).json({ error: body.error.errors });
            return;
        }

        const { x, y, title, description, color, icon } = body.data;

        const result = await tryCatch(db.insert(markers).values({ x, y, title, description, color, icon, mapId }));

        if (result.error) {
            logger("ERROR", `Failed to add marker to map: ${result.error}`);
            res.status(500).json({ error: "Failed to add marker to map" });
            return;
        }

        logger("INFO", `Marker added to map with ID: ${mapId}`);
        res.status(201).json({ id: result.data.lastInsertRowid });
    });

    router.patch("/api/maps/:id/markers/:markerId", async (req, res) => {
        logger("INFO", `PATCH /api/maps/${req.params.id}/markers/${req.params.markerId} called`);

        const authRes = await auth(req);
        if (!authRes) {
            logger("WARN", "Unauthorized access attempt to update marker on map");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        if (Number.isNaN(req.params.id)) {
            logger("WARN", `Invalid map ID: ${req.params.id}`);
            res.status(400).json({ error: "Map id is required and needs to be an int" });
            return;
        }

        const mapId = parseInt(req.params.id);

        if (Number.isInteger(req.params.markerId)) {
            logger("WARN", `Invalid marker ID: ${req.params.markerId}`);
            res.status(400).json({ error: "Marker id is required and needs to be an int" });
            return;
        }

        const markerId = parseInt(req.params.markerId);

        // check if the map exists and belongs to the user
        const mapCheckResult = await tryCatch(
            db
                .select({ id: maps.id })
                .from(maps)
                .where(and(eq(maps.id, mapId), eq(maps.userId, authRes.user.id))),
        );

        if (mapCheckResult.error) {
            logger("ERROR", `Failed to check map existence: ${mapCheckResult.error}`);
            res.status(500).json({ error: "Failed to check map existence" });
            return;
        }

        const body = z
            .object({
                x: z.number().optional(),
                y: z.number().optional(),
                title: z.string().optional(),
                description: z.string().optional(),
                color: z.string().optional(),
                icon: z.string().optional(),
            })
            .safeParse(req.body);
        if (!body.success) {
            logger("WARN", `Validation failed: ${JSON.stringify(body.error.errors)}`);
            res.status(400).json({ error: body.error.errors });
            return;
        }

        const { x, y, title, description, color, icon } = body.data;

        const updateData: any = {};
        if (x !== undefined) updateData.x = x;
        if (y !== undefined) updateData.y = y;
        if (title !== undefined) updateData.title = title;
        if (description !== undefined) updateData.description = description;
        if (color !== undefined) updateData.color = color;
        if (icon !== undefined) updateData.icon = icon;

        const result = await tryCatch(db.update(markers).set(updateData).where(eq(markers.id, markerId)));

        if (result.error) {
            logger("ERROR", `Failed to update marker on map: ${result.error}`);
            res.status(500).json({ error: "Failed to update marker on map" });
            return;
        }

        if (result.data.rowsAffected === 0) {
            logger("WARN", `Marker not found with ID: ${markerId}`);
            res.status(404).json({ error: "Marker not found" });
            return;
        }

        logger("INFO", `Marker updated on map with ID: ${mapId}`);
        res.status(200).json({ message: "Marker updated successfully" });
    });

    router.delete("/api/maps/:id/markers/:markerId", async (req, res) => {
        logger("INFO", `DELETE /api/maps/${req.params.id}/markers/${req.params.markerId} called`);

        const authRes = await auth(req);
        if (!authRes) {
            logger("WARN", "Unauthorized access attempt to delete marker from map");
            res.status(401).json({ error: "Unauthorized" });
            return;
        }

        if (Number.isNaN(req.params.id)) {
            logger("WARN", `Invalid map ID: ${req.params.id}`);
            res.status(400).json({ error: "Map id is required and needs to be an int" });
            return;
        }

        const mapId = parseInt(req.params.id);

        if (Number.isInteger(req.params.markerId)) {
            logger("WARN", `Invalid marker ID: ${req.params.markerId}`);
            res.status(400).json({ error: "Marker id is required and needs to be an int" });
            return;
        }




        // check if the map exists and belongs to the user
        const mapCheckResult = await tryCatch(
            db
                .select({ id: maps.id })
                .from(maps)
                .where(and(eq(maps.id, mapId), eq(maps.userId, authRes.user.id))),
        );

        if (mapCheckResult.error) {
            logger("ERROR", `Failed to check map existence: ${mapCheckResult.error}`);
            res.status(500).json({ error: "Failed to check map existence" });
            return;
        }

        const markerId = parseInt(req.params.markerId);

        const result = await tryCatch(db.delete(markers).where(eq(markers.id, markerId)));

        if (result.error) {
            logger("ERROR", `Failed to delete marker from map: ${result.error}`);
            res.status(500).json({ error: "Failed to delete marker from map" });
            return;
        }

        if (result.data.rowsAffected === 0) {
            logger("WARN", `Marker not found with ID: ${markerId}`);
            res.status(404).json({ error: "Marker not found" });
            return;
        }

        logger("INFO", `Marker deleted from map with ID: ${mapId}`);
        res.status(200).json({ message: "Marker deleted successfully" });
    });

    return router;
}

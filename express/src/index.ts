import express from "express";
import cookieParser from "cookie-parser";
import cors from "cors";
import { createServer } from "http";
import env from "./env";
import getLogger from "./utils/logger";
import { userRouter } from "./router/user";
import { mapsRouter } from "./router/maps";
import { accountRouter } from "./router/account";

const logger = getLogger("main");

const app = express()
    .use(
        cors({
            origin: env.SERVER_CORS_ORIGINS.split(",").map((origin) => origin.trim()),
            methods: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            optionsSuccessStatus: 204,
            allowedHeaders: [
                "Content-Type",
                "Authorization",
                "X-Requested-With",
                "Accept",
                "Origin",
                "Access-Control-Allow-Credentials",
            ],
            credentials: true,
        }),
    )
    .use(express.json())
    .use(cookieParser())
    .use(userRouter())
    .use(mapsRouter())
    .use(accountRouter());

createServer(app).listen(env.SERVER_PORT, () => {
    logger("INFO", `Server is running on port ${env.SERVER_PORT}`);
});

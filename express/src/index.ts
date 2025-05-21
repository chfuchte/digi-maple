import express from "express";
import cookieParser from "cookie-parser";
import cors from "cors";
import { createServer as createHTTPServer } from "http";
import env from "./env";
import getLogger from "./utils/logger";
import { userRouter } from "./router/user";
import { mapsRouter } from "./router/maps";
import { accountRouter } from "./router/account";

const logger = getLogger("main");

const app = express()
    .use(
        cors({
            origin: env.FRONTEND_URL,
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
    .use(accountRouter())
    .use(express.static(env.ABSOLUTE_FRONTEND_DIR));

createHTTPServer(app).listen(env.PORT, () => {
    logger("INFO", `Server is running on port http://localhost:${env.PORT}`);
});

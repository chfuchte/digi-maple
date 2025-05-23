import { z } from "zod";

const envSchema = z.object({
    LOG_DIR_PATH: z.string(),
    IMAGES_DIR_PATH: z.string(),
    SERVER_CORS_ORIGINS: z.string(),
    SERVER_PORT: z.string(),
    SERVER_URL: z.string(),
    DATABASE_URL: z.string(),
    DATABASE_AUTH_TOKEN: z.string(),
});

export default envSchema.parse(process.env);

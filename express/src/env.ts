import { join } from "node:path";
import { z } from "zod";

const envSchema = z.object({
    LOG_DIR: z.string(),
    PORT: z.string(),
    ABSOLUTE_FRONTEND_DIR: z.string().default(join(__dirname, "../public")),
    ABSOLUTE_IMAGES_DIR: z.string().default(join(__dirname, "../images")),
    FRONTEND_URL: z.string(),
    DATABASE_URL: z.string(),
    DATABASE_AUTH_TOKEN: z.string(),
});

export default envSchema.parse(process.env);

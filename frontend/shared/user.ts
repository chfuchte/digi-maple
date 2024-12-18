import { z } from "zod";

const userSchema = z.object({
    id: z.number(),
    username: z.string(),
    email: z.string().email(),
});

const usersSchema = z.array(userSchema);

type User = z.infer<typeof userSchema>;

export { type User, userSchema, usersSchema };

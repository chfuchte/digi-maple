import { fetcher } from "@/lib/fetch";
import { tryCatch } from "@/lib/utils";
import { z } from "zod";

export async function apiLogin(email: string, password: string): Promise<boolean> {
    const res = await tryCatch(
        fetcher.post("http://localhost:8080/api/auth/login", {
            email: email,
            password: password,
        }),
    );

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiRegister(email: string, password: string, fullName: string): Promise<boolean> {
    const res = await tryCatch(
        fetcher.post("http://localhost:8080/api/auth/register", {
            email: email,
            password: password,
            full_name: fullName,
        }),
    );

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiLogout(): Promise<boolean> {
    const res = await tryCatch(fetcher.post("http://localhost:8080/api/auth/logout"));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiWhoami(): Promise<
    | {
          email: string;
          full_name: string;
          id: number;
      }
    | false
> {
    const res = await tryCatch(
        fetcher.get("http://localhost:8080/api/auth/whoami", {
            withCredentials: true,
        }),
    );

    if (res.error) {
        return false;
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z
        .object({
            email: z.string(),
            full_name: z.string(),
            id: z.number(),
        })
        .safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

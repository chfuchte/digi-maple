import { tryCatch } from "@/lib/utils";
import axios from "axios";

export async function apiDeleteUser(): Promise<boolean> {
    const res = await tryCatch(axios.delete("http://localhost:8080/api/auth/user"));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiUpdateUser(data: {
    full_name?: string;
    email?: string;
    password?: string;
}): Promise<boolean> {
    const res = await tryCatch(axios.patch("http://localhost:8080/api/auth/user", data));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

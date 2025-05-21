import { fetcher } from "@/lib/fetch";
import { tryCatch } from "@/lib/utils";

export async function apiChangePassword(oldPassword: string, newPassword: string): Promise<boolean> {
    const res = await tryCatch(
        fetcher.patch("http://localhost:8080/api/account/chpwd", {
            old_password: oldPassword,
            new_password: newPassword,
        }),
    );

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiChangeEmail(email: string, password: string): Promise<boolean> {
    const res = await tryCatch(
        fetcher.patch("http://localhost:8080/api/account/chemail", {
            email: email,
            password: password,
        }),
    );

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiChangeName(name: string): Promise<boolean> {
    const res = await tryCatch(
        fetcher.patch("http://localhost:8080/api/account/chname", {
            full_name: name,
        }),
    );

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiDeleteAccount(password: string): Promise<boolean> {
    const res = await tryCatch(
        fetcher.delete("http://localhost:8080/api/account", {
            data: {
                password: password,
            },
        }),
    );

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

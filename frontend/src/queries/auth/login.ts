import { makePOST } from "@/lib/utils";

export async function apiLogin(email: string, password: string): Promise<boolean> {
    try {
        const { status, data } = await makePOST<{ access_token: string; token_type: "Bearer" }>(
            "http://localhost:8080/auth/login",
            {
                email,
                password,
            },
        );

        if (status === 200) {
            localStorage.setItem("auth_token", data.access_token);
            return true;
        } else {
            return false;
        }
    } catch {
        return false;
    }
}

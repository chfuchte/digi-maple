import { makePOST } from "@/lib/utils";

export async function apiLogout(): Promise<boolean> {
    try {
        const { status } = await makePOST("http://localhost:8080/auth/logout", {});

        return status === 200;
    } catch {
        return false;
    }
}

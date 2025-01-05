import { makePOST } from "~/shared/make-query"

export async function apiRegister(fullName: string, email: string, password: string): Promise<boolean> {
    try {
        const { status } = await makePOST("http://localhost:8080/auth/register", {
            full_name: fullName,
            email,
            password
        })

        return status === 200
    } catch {
        return false
    }
}
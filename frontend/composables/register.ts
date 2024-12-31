export async function apiRegister(fullName: string, email: string, password: string): Promise<boolean> {
    try {
        const res = await $fetch<{ success: boolean }>("http://localhost:8080/auth/register", {
            method: "POST",
            body: JSON.stringify({ fullName, email, password }),
            headers: {
                "Content-Type": "application/json"
            }
        })

        return res.success ?? false
    } catch {
        return false
    }
}
export async function apiLogin(email: string, password: string): Promise<boolean> {
    try {
        const res = await $fetch<{ success: boolean }>("http://localhost:8080/auth/login", {
            method: "POST",
            body: JSON.stringify({ email, password }),
            headers: {
                "Content-Type": "application/json"
            }
        })

        return res.success ?? false
    } catch {
        return false
    }
}
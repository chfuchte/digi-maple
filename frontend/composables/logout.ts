import axios from "axios"

export async function apiLogout(): Promise<boolean> {
    try {
        const { status } = await axios.post("http://localhost:8080/auth/logout", undefined, {
            headers: {
                "Content-Type": "application/json"
            },
            withCredentials: true
        })

        return status === 200
    } catch {
        return false
    }
}
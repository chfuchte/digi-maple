import axios from "axios"

export async function apiRegister(fullName: string, email: string, password: string): Promise<boolean> {
    try {
        const { status } = await axios.post("http://localhost:8080/auth/register", {
            full_name: fullName,
            email,
            password
        }, {
            headers: {
                "Content-Type": "application/json"
            }
        })

        return status === 200
    } catch {
        return false
    }
}
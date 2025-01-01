import axios from "axios";

export async function apiLogin(email: string, password: string): Promise<boolean> {
    try {
        const { status, headers } = await axios.post("http://localhost:8080/auth/login", {
            email,
            password
        }, {
            headers: {
                "Content-Type": "application/json"
            }
        })

        if (status === 200) {
            document.cookie += headers["set-cookie"]
            return true
        } else {
            return false
        }
    } catch {
        return false
    }
}
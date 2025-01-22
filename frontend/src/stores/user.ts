import { makeGET } from "@/lib/utils";
import { apiLogout } from "@/queries/auth/logout";
import { userSchema, type User } from "@/schema/user";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCurrentUserStore = defineStore("currentUser", () => {
    const currentUser = ref<User | null>(null);
    const lastFetched = ref<number>(0);

    const fetch = async () => {
        try {
            const res = await makeGET("http://localhost:8080/auth/whoami");

            if (res.status === 200) {
                const user = userSchema.parse(res.data);
                currentUser.value = user;
            } else {
                currentUser.value = null;
            }
        } catch {
            currentUser.value = null;
        }

        lastFetched.value = Date.now();
    };

    const getUser = () => {
        if (currentUser.value === null || Date.now() - lastFetched.value > 1000 * 60 * 5) {
            // 5 min
            fetch();
        }
        return currentUser.value;
    };

    const logout = async () => {
        await apiLogout();
        currentUser.value = null;
    };

    return { fetch, getUser, logout };
});

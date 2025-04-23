import { apiLogout, apiWhoami } from "@/queries/auth";
import type { User } from "@/typings/user";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCurrentUserStore = defineStore("currentUser", () => {
    const currentUser = ref<User | null>(null);
    const lastFetched = ref<number>(0);

    const fetch = async () => {
        try {
            const user = await apiWhoami();
            if (user) {
                currentUser.value = user;
            } else {
                currentUser.value = null;
            }
        } catch {
            currentUser.value = null;
        }

        lastFetched.value = Date.now();
    };

    const getUser = async () => {
        if (currentUser.value === null || Date.now() - lastFetched.value > 1000 * 60 * 5) {
            // 5 min
            await fetch();
        }
        return currentUser.value;
    };

    const logout = async () => {
        await apiLogout();
        currentUser.value = null;
    };

    return { fetch, getUser, logout };
});

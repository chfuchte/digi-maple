import { makeGET } from "~/shared/make-query";
import { userSchema, type User } from "~/shared/user";

export const useCurrentUserStore = defineStore('currentUser', () => {
    const currentUser = ref<User | null>(null);
    const lastFetched = ref<number>(0);

    const fetch = async () => {
        const res = await makeGET("http://localhost:8080/auth/whoami");

        if (res.status === 200) {
            try {
                const user = userSchema.parse(res.data);
                currentUser.value = user;
            } catch (e) {
                currentUser.value = null;
            }
        } else {
            currentUser.value = null;
        }

        lastFetched.value = Date.now();
    }

    const getUser = () => {
        if (currentUser.value === null || Date.now() - lastFetched.value > 1000 * 60 * 5) { // 5 min
            fetch();
        }
        return currentUser.value;
    }

    const logout = async () => {
        await apiLogout();
        currentUser.value = null;
    }

    return { fetch, getUser, logout };
});
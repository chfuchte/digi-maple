import { userSchema, type User } from "~/shared/user";

export const useCurrentUserStore = defineStore('currentUser', () => {
    const currentUser = ref<User | null>(null);
    const lastFetched = ref<number>(0);

    const fetch = async () => {
        const {
            clear, data, error, status
        } = await useAsyncData("currentUser", () => $fetch<User>("http://localhost:8080/whoami"));

        if (status.value === "success") {
            const user = userSchema.parse(data);
            currentUser.value = user;
        } else if (status.value === "error" || error.value !== null) {
            clear();
            currentUser.value = null;
        }

        lastFetched.value = Date.now();
    }

    const getUser = () => {
        console.log("hi");
        if (currentUser.value === null || Date.now() - lastFetched.value > 1000 * 60 * 5) { // 5 min
            fetch();
        }
        return currentUser.value;
    }

    const logout = async () => {
        await $fetch("http://localhost:8080/auth/logout");
        currentUser.value = null;
    }

    return { fetch, getUser, logout };
});
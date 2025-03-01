import { createRouter, createWebHistory } from "vue-router";
import IndexPage from "@/pages/index.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    linkActiveClass: "dark:!text-white !text-black",
    routes: [
        {
            path: "/",
            name: "Welcome to Maple",
            component: IndexPage,
        },
        {
            path: "/auth",
            name: "Anmelden",
            component: () => import("../pages/auth/index.vue"),
        },
        {
            path: "/dashboard",
            name: "Dashboard",
            component: () => import("../pages/dashboard.vue"),
        },
        {
            path: "/account/general",
            name: "General account settings",
            component: () => import("../pages/account/general.vue"),
        },
        {
            path: "/account/security",
            name: "Security account settings",
            component: () => import("../pages/account/security.vue"),
        },
        {
            path: "/edit",
            name: "Edit a map",
            component: () => import("../pages/edit.vue"),
        },
        {
            path: "/create",
            redirect: "/edit",
        },
    ],
});

export default router;

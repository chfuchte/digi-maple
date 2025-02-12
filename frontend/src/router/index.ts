import { createRouter, createWebHistory } from "vue-router";
import IndexPage from "@/pages/index.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
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
            path: "/edit",
            name: "Edit a map",
            component: () => import("../pages/edit.vue"),
        },
        {
            path: "/create",
            redirect: "/edit",
        },
        {
            path: "/maps/dev",
            name: "Dev Map View",
            component: () => import("../pages/maps/dev.vue"),
        },
    ],
});

export default router;

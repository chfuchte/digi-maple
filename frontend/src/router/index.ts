import { createRouter, createWebHistory } from "vue-router";
import IndexPage from "@/pages/index.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    linkActiveClass: "dark:!text-white !text-black",
    routes: [
        {
            path: "/",
            component: IndexPage,
        },
        {
            path: "/auth",
            component: () => import("../pages/auth/index.vue"),
        },
        {
            path: "/dashboard",
            component: () => import("../pages/dashboard.vue"),
        },
        {
            path: "/map/:id",
            component: () => import("../pages/map/[id]/index.vue"),
        },
        {
            path: "/map/:id/edit",
            component: () => import("../pages/map/[id]/edit.vue"),
        },
    ],
});

export default router;

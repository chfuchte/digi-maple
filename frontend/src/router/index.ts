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
            path: "/maps/:id/edit",
            component: () => import("../pages/maps/[id]/edit.vue"),
        },
        {
            path: "/maps/:id",
            component: () => import("../pages/maps/[id]/index.vue"),
        },
        {
            path: "/account",
            component: () => import("../pages/account.vue"),
        }
    ],
});

export default router;

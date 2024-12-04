// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: "2024-04-03",
    app: {
        head: {
            bodyAttrs: {
                class: "",
            },
        },
    },
    ssr: true,
    routeRules: {},
    css: ["~/assets/css/global.css"],
    modules: [
        "@vueuse/nuxt",
        "@nuxtjs/tailwindcss",
        "shadcn-nuxt",
        "@nuxtjs/color-mode",
        "@nuxtjs/leaflet",
        "nuxt-lucide-icons",
    ],
    shadcn: {
        /**
         * Prefix for all the imported component
         */
        prefix: "",
        /**
         * Directory that the component lives in.
         * @default "./components/ui"
         */
        componentDir: "./components/ui",
    },
    tailwindcss: {
        exposeConfig: true,
        viewer: false,
        configPath: "./tailwind.config",
        cssPath: "./assets/css/global.css",
    },
    $development: {
        devtools: { enabled: true },
        tailwindcss: {
            viewer: true,
        },
    },
});

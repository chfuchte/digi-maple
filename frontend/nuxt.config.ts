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
    ssr: false,
    css: ["~/assets/css/global.css"],
    modules: [
      "@vueuse/nuxt",
      "@nuxtjs/tailwindcss",
      "shadcn-nuxt",
      "@nuxtjs/color-mode",
      "@nuxtjs/leaflet",
      "nuxt-lucide-icons",
      "@pinia/nuxt",
    ],
    colorMode: {
        classSuffix: "",
        classPrefix: "",
    },
    shadcn: {
        prefix: "",
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
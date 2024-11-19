// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: "2024-04-03",
    app: {
        head: {
            bodyAttrs: {
                class: "dark",
            }
        }
    },
    css: ["~/assets/css/global.css"],
    modules: ['@vueuse/nuxt', "@nuxtjs/tailwindcss", "@nuxt/eslint"],
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
    ssr: true,
});
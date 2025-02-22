import { createApp } from "vue";
import { createPinia } from "pinia";
import { createHead } from "@unhead/vue";
import App from "./App.vue";
import router from "./router";

import "./styles/globals.css";

createApp(App).use(createPinia()).use(router).use(createHead()).mount("#root");

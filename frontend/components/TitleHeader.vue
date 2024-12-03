<script setup lang="ts">
import { Map } from "lucide-vue-next";

const { title = "" } = defineProps<{
    title?: string;
}>();
</script>

<template>
    <header class="bg-white border-b-2 border-b-black text-black flex items-center justify-between px-4">
        <div class="flex items-center gap-3 my-2">
            <div class="flex items-center gap-1">
                <Map :size="30" />
                <h1 class="text-3xl">Maple</h1>
            </div>
            <div v-if="title != ''" class="w-0.5 h-5 bg-black"></div>
            <h3>
                {{ title }}
            </h3>
        </div>
        <slot />
    </header>
</template>

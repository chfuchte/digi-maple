<script setup lang="ts">
import { Toaster } from '@/components/ui/sonner'
import { useColorMode } from "@vueuse/core";
import { RouterView } from "vue-router";

useColorMode({
    initialValue: "auto",
    attribute: "class",
    selector: "html",
});
</script>

<template>
    <RouterView />

    <Toaster rich-colors />
</template>

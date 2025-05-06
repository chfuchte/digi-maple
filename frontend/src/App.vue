<script setup lang="ts">
import { useColorMode } from "@vueuse/core";
import { RouterView } from "vue-router";
import { Toaster } from "@/components/ui/sonner";

useColorMode({
    initialValue: "auto",
    attribute: "class",
    selector: "html",
});
</script>

<template>
    <Toaster richColors class="pointer-events-auto" />
    <RouterView />
</template>

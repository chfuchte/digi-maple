<script setup lang="ts">
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
</template>

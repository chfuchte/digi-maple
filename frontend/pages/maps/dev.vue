<script setup lang="ts">
import devMapImagePath from "@/assets/dev/Lageplan_Campus_Bockenheim.svg";

const imageHeightWidthRatio = 0.94285675588;
const height = 2000;
const width = imageHeightWidthRatio * height;

useHead({
    title: "Dev Map",
})
</script>

<template>
    <ClientOnly fallback="Loading...">
        <MapView :map-img-url="devMapImagePath" :map-img-width="width" :map-imgheight="height" />
    </ClientOnly>
</template>

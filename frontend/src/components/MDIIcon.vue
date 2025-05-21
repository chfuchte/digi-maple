<script setup lang="ts">
const props = defineProps<{
    size?: number;
    path: string;
}>();
</script>

<template>
    <svg :width="props.size ?? 24" :height="props.size ?? 24" viewBox="0 0 24 24">
        <path :d="path" />
    </svg>
</template>

<style scoped>
path {
    fill: currentColor;
}
</style>

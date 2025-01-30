<script setup lang="ts">
import { LucideAccessibility } from "lucide-vue-next";

const props = defineProps<{
    size?: number;
}>();
</script>

<template>
    <LucideAccessibility :size="props.size" />
</template>

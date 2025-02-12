<script setup lang="ts">
import { LucideAlertTriangle } from "lucide-vue-next";

const props = defineProps<{
    size?: number;
}>();
</script>

<template>
    <LucideAlertTriangle :size="props.size ?? 18" />
</template>

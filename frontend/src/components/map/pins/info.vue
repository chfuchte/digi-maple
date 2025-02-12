<script setup lang="ts">
import { LucideInfo } from "lucide-vue-next";

const props = defineProps<{
    size?: number;
}>();
</script>

<template>
    <LucideInfo :size="props.size ?? 18" />
</template>

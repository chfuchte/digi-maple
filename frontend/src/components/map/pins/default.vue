<script setup lang="ts">
import { LucidePin } from "lucide-vue-next";

const props = defineProps<{
    size?: number;
}>();
</script>

<template>
    <LucidePin :size="props.size ?? 18" />
</template>

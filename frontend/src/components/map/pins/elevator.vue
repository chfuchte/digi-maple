<script setup lang="ts">
import MDIIcon from "@/components/MDIIcon.vue";
import { mdiElevatorPassengerOutline } from "@mdi/js";

const props = defineProps<{
    size?: number;
}>();
</script>

<template>
    <MDIIcon :size="props.size ?? 18" :path="mdiElevatorPassengerOutline" />
</template>

<script setup lang="ts">
import { Button } from "../ui/button";
import { LucideZoomIn, LucideZoomOut } from "lucide-vue-next";

const props = defineProps<{
    zoomInDisabled: boolean;
    zoomOutDisabled: boolean;
}>();

const emit = defineEmits(["zoomIn", "zoomOut"]);
</script>

<template>
    <div class="flex flex-col gap-1 rounded-md border bg-background p-1.5">
        <Button @click="emit('zoomIn')" :disabled="props.zoomInDisabled" variant="secondary">
            <LucideZoomIn />
        </Button>
        <Button @click="emit('zoomOut')" :disabled="props.zoomOutDisabled" variant="secondary">
            <LucideZoomOut />
        </Button>
    </div>
</template>

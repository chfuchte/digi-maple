<script setup lang="ts">
const props = defineProps<{
    zoomIndisabled: boolean;
    zoomOutDisabled: boolean;
}>();

const emit = defineEmits(["zoomIn", "zoomOut"]);
</script>

<template>
    <div class="flex flex-col gap-1 rounded-md border border-black bg-white p-1.5 backdrop-blur">
        <Button @click="emit('zoomIn')" :disabled="props.zoomIndisabled" variant="secondary">
            <LucideZoomIn />
        </Button>
        <Button @click="emit('zoomOut')" :disabled="props.zoomOutDisabled" variant="secondary">
            <LucideZoomOut />
        </Button>
    </div>
</template>

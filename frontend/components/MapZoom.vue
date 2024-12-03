<script setup lang="ts">
const props = defineProps<{
    disableZoomIn: boolean;
    disableZoomOut: boolean;
}>();

const emit = defineEmits(["zoomIn", "zoomOut"]);
</script>

<template>
    <div class="flex flex-col gap-1 bg-white backdrop-blur p-1.5 rounded-md border-black">
        <Button @click="emit('zoomIn')" :disabled="props.disableZoomIn" variant="secondary">
            <LucideChevronUp />
        </Button>
        <Button @click="emit('zoomOut')" :disabled="props.disableZoomOut" variant="secondary">
            <LucideChevronDown />
        </Button>
    </div>
</template>

<style scoped>
div {
    border-width: 1px;
}
</style>
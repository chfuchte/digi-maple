<script setup lang="ts">
import MapIconPin from "@/components/map/pins/index.vue";
import type { MapPinType } from "@/typings/map";

const props = defineProps<{
    title: string;
    content: string;
    icon: MapPinType;
}>();
</script>

<template>
    <div class="flex h-auto w-40 flex-col items-start justify-start gap-2">
        <h4 class="inline-flex gap-1 font-bold">
            <MapIconPin :size="18" :variant="props.icon" />
            {{ props.title }}
        </h4>
        <span>
            {{ props.content }}
        </span>
    </div>
</template>

<script setup lang="ts">
import type { MapMarker } from "@/schema/mapView";
import { LucideAccessibility, LucideAlertTriangle, LucideInfo, LucidePin } from "lucide-vue-next";

const props = defineProps<{
    title: string;
    content: string;
    icon: MapMarker["display"]["markerType"];
}>();
</script>

<template>
    <div class="flex h-auto w-40 flex-col items-start justify-start gap-2">
        <h4 class="inline-flex gap-1 font-bold">
            <!-- TODO: imports! -->
            <LucideAccessibility v-if="icon == 'weelchair'" :size="18" />
            <LucideAlertTriangle v-else-if="icon == 'warning'" :size="18" />
            <LucideInfo v-else-if="icon == 'info'" :size="18" />
            <LucidePin v-else :size="18" />
            {{ props.title }}
        </h4>
        <span>
            {{ props.content }}
        </span>
    </div>
</template>

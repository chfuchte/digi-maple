<script setup lang="ts">
import type { MapMarker } from '~/shared/mapView';


const props = defineProps<{
    title: string;
    content: string;
    icon: MapMarker["display"]["markerType"];
}>();

</script>

<template>
    <div class="w-40 h-auto flex items-start justify-start flex-col gap-2">
        <h4 class="font-bold inline-flex gap-1">
            <LazyLucideAccessibility v-if="icon == 'weelchair'" :size="18" />
            <LazyLucideAlertTriangle v-else-if="icon == 'warning'" :size="18" />
            <LazyLucideInfo v-else-if="icon == 'info'" :size="18" />
            <LazyLucidePin v-else :size="18" />
            {{ props.title }}
        </h4>
        <span>
            {{ props.content }}
        </span>
    </div>
</template>
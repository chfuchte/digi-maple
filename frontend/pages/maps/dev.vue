<script setup lang="ts">
import type { MapView } from "@/shared/mapView";

definePageMeta({
    middleware: 'auth'
});

let mapProps: Ref<MapView | undefined> = ref<MapView | undefined>(undefined);

onBeforeMount(async () => {
    if (import.meta.client) {
        // Ensures this runs only on the client side
        try {
            const res = await fetchEverything();
            mapProps.value = res.maps[0];
            useHead({
                title: mapProps.value?.name ?? "Error",
            });
        } catch (error) {
            console.error(error);
            useHead({
                title: mapProps.value?.name ?? "Error",
            });
        }
    }
});
</script>

<template>
    <ClientOnly fallback="Loading...">
        <div v-if="!mapProps" class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
            <h2 class="font-bold text-2xl">Error loading map</h2>
        </div>

        <MapView v-else :map-img-url="mapProps.imgUrl" :map-img-width="mapProps.imgWidth"
            :map-imgheight="mapProps.imgHeight" :markers="mapProps.markers" />
    </ClientOnly>
</template>

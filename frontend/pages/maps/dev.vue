<script setup lang="ts">
import type { MapView } from "@/shared/mapView";

let mapProps: Ref<MapView | undefined> = ref<MapView | undefined>(undefined);

onBeforeMount(async () => {
    if (import.meta.client) { // Ensures this runs only on the client side
        try {
            const res = await fetchEverything();
            mapProps.value = res.maps[0];
            useHead({
                title: mapProps.value?.name ?? "Error",
            });
        } catch (error) {
            console.error(error);
            alert("Error while fetching data"); useHead({
                title: mapProps.value?.name ?? "Error",
            });
        }
    }
});
</script>

<template>
    <ClientOnly fallback="Loading...">
        <h2 v-if="!mapProps">
            Error loading map
        </h2>

        <MapView v-else :map-img-url="mapProps.imgUrl" :map-img-width="mapProps.imgWidth"
            :map-imgheight="mapProps.imgHeight" :markers="mapProps.markers" />
    </ClientOnly>
</template>

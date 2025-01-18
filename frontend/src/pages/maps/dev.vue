<script setup lang="ts">
import fetchEverything from "@/queries/fetchEverything";
import type { MapView as MapViewType } from "@/schema/mapView";
import { onBeforeMount, ref, type Ref } from "vue";
import { useHead } from "@unhead/vue";
import Layout from "@/components/layouts/default.vue";
import MapView from "@/components/map/View.vue";

const mapProps: Ref<MapViewType | undefined> = ref<MapViewType | undefined>(undefined);

onBeforeMount(async () => {
    try {
        const res = await fetchEverything();
        mapProps.value = res[0];
        useHead({
            title: mapProps.value?.name ?? "Error",
        });
    } catch (error) {
        console.error(error);
        useHead({
            title: mapProps.value?.name ?? "Error",
        });
    }
});
</script>

<template>
    <Layout>
        <div v-if="!mapProps" class="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
            <h2 class="text-2xl font-bold">Error loading map</h2>
        </div>

        <MapView v-else :map-img-url="mapProps.imgUrl" :map-img-width="mapProps.imgWidth"
            :map-imgheight="mapProps.imgHeight" :markers="mapProps.markers" />
    </Layout>
</template>

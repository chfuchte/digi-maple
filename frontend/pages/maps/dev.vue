<script setup lang="ts">
import type { MapView } from "@/shared/mapView";
import devMapImagePath from "@/assets/dev/Lageplan_Campus_Bockenheim.svg";

const mapProps: MapView = {
    name: "Dev Map",
    author: "Devs",
    imgUrl: devMapImagePath,
    imgWidth: 2000 * 0.94285675588,
    imgHeight: 2000,
    markers: [
        {
            id: "0000-0000-0001",
            x: 1000 * 0.94285675588,
            y: 1000,
            display: {
                title: "Marker 1",
                description: "Somedescription",
                markerType: "favicon",
            },
        },
    ],
};

useHead({
    title: "Dev Map",
});
</script>

<template>
    <ClientOnly fallback="Loading...">
        <MapView
            :map-img-url="mapProps.imgUrl"
            :map-img-width="mapProps.imgWidth"
            :map-imgheight="mapProps.imgHeight"
            :markers="mapProps.markers" />
    </ClientOnly>
</template>

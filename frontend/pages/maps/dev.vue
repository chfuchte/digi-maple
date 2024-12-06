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
                title: "Wuhu",
                description: "Ich bin ein Marker",
                markerType: "default",
            },
        },
        {
            id: "0000-0000-0001",
            x: 1000 * 0.94285675588,
            y: 800,
            display: {
                title: "Sekretariat",
                description: "Get some help here",
                markerType: "info",
            },
        },
        {
            id: "0000-0000-0001",
            x: 1000 * 0.94285675588,
            y: 600,
            display: {
                title: "Achtung",
                description: "Viele Besucher",
                markerType: "warning",
            },
        },
        {
            id: "0000-0000-0001",
            x: 1000 * 0.94285675588,
            y: 400,
            display: {
                title: "Eingang zum Gebäude",
                description: "Barrierefreier Eingang zum Gebäude",
                markerType: "weelchair",
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

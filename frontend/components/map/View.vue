<script setup lang="ts">
import { ref } from "vue";
import { latLngBounds, CRS, Map } from "leaflet";

const props = defineProps<{
    mapImgUrl: string;
    mapImgWidth: number;
    mapImgheight: number;
    markers?: Array<{
        name?: string;
        lng: number;
        lat: number;
    }>;
}>();

const zoomInDisabled = ref(false);
const zoomOutDisabled = ref(true);
const zoomLevel = ref<number>(-2);

let leafletObject = ref<Map>();

const onMapReady = (map: Map) => {
    leafletObject.value = map;
    zoomLevel.value = map.getZoom();
};

const handleZoomEvent = (newZoomLevel: number) => {
    zoomLevel.value = newZoomLevel;
    zoomInDisabled.value = zoomLevel.value == leafletObject.value?.getMaxZoom();
    zoomOutDisabled.value = zoomLevel.value == leafletObject.value?.getMinZoom();
};

const bounds = latLngBounds([0, 0], [props.mapImgWidth, props.mapImgheight]);
</script>

<template>
    <LMap
        ref="map"
        :zoom="zoomLevel"
        :center="[bounds.getCenter().lat, bounds.getCenter().lng]"
        :crs="CRS.Simple"
        :min-zoom="-2"
        :max-zoom="2"
        :options="{
            zoomControl: false,
            attributionControl: false,
        }"
        @ready="onMapReady"
        @update:zoom="handleZoomEvent">
        <LControl position="bottomleft">
            <MapZoomButtons
                @zoom-in="leafletObject?.zoomIn()"
                @zoom-out="leafletObject?.zoomOut()"
                :zoom-indisabled="zoomInDisabled"
                :zoom-out-disabled="zoomOutDisabled" />
        </LControl>
        <LImageOverlay :url="props.mapImgUrl!" :bounds />
        <LMarker v-for="marker in markers" :key="marker.name ?? ''" :lat-lng="marker">
            <LPopup :content="marker.name ?? ''" />
        </LMarker>
    </LMap>
</template>

<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LControl, LImageOverlay, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import MapPopup from "@/components/map/Popup.vue";
import MapZoomButtons from "@/components/map/ZoomButtons.vue";
import { ref } from "vue";
import { latLngBounds, CRS, Map } from "leaflet";
import type { MapMarker } from "@/schema/mapView";
import { getLIconFromString } from "@/lib/getLIconFromString";

const props = defineProps<{
    mapImgUrl: string;
    mapImgWidth: number;
    mapImgheight: number;
    markers?: Array<MapMarker>;
}>();

const zoomInDisabled = ref(false);
const zoomOutDisabled = ref(true);
const zoomLevel = ref<number>(-2);

const leafletObject = ref<Map>();

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
    <LMap ref="map" :zoom="zoomLevel" :center="[bounds.getCenter().lat, bounds.getCenter().lng]" :crs="CRS.Simple"
        :min-zoom="-2" :max-zoom="2" :options="{
            zoomControl: false,
            attributionControl: false,
        }" @ready="onMapReady" @update:zoom="handleZoomEvent">
        <LControl position="bottomleft">
            <MapZoomButtons @zoom-in="leafletObject?.zoomIn(0.5)" @zoom-out="leafletObject?.zoomOut(0.5)"
                :zoom-indisabled="zoomInDisabled" :zoom-out-disabled="zoomOutDisabled" />
        </LControl>
        <LImageOverlay :url="props.mapImgUrl!" :bounds />
        <LMarker :icon="getLIconFromString(marker.display.markerType)" v-for="marker in markers" :key="marker.id"
            :lat-lng="[marker.x, marker.y]">
            <LPopup>
                <MapPopup :title="marker.display.title" :icon="marker.display.markerType"
                    :content="marker.display.description"></MapPopup>
            </LPopup>
        </LMarker>
    </LMap>
</template>

<style>
.leaflet-popup-content-wrapper {
    background: none;
    box-shadow: none;
}

.leaflet-popup-content {
    padding: 10px !important;
    margin: 0 !important;
    width: 100% !important;
    background-color: #f0f0f0;
    border: none;
    border-radius: 10px;
}
</style>

<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LControl, LImageOverlay, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import MapPopup from "@/components/map/Popup.vue";
import MapZoomButtons from "@/components/map/ZoomButtons.vue";
import { ref } from "vue";
import { latLngBounds, CRS, Map } from "leaflet";
import type { MapPinType, Marker } from "@/typings/map";
import { LucideMapPin } from "lucide-vue-next";
import { LIcon } from "@vue-leaflet/vue-leaflet";

const props = defineProps<{
    mapImgUrl: string;
    mapImgWidth: number;
    mapImgheight: number;
    markers?: Array<Marker>;
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

const bounds = latLngBounds([0, 0], [2000, (props.mapImgWidth / props.mapImgheight) * 2000]);
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
                @zoom-in="leafletObject?.zoomIn(1)"
                @zoom-out="leafletObject?.zoomOut(1)"
                :zoom-in-disabled="zoomInDisabled"
                :zoom-out-disabled="zoomOutDisabled" />
        </LControl>
        <LImageOverlay :url="props.mapImgUrl!" :bounds />
        <LMarker v-for="marker in markers" :key="marker.id" :lat-lng="[marker.x, marker.y]">
            <LIcon :iconSize="[42, 42]" class-name="border-none outline-none">
                <LucideMapPin class="fill-blue-500" :size="42" />
            </LIcon>
            <LPopup>
                <MapPopup
                    :title="marker.title"
                    :icon="marker.icon as MapPinType"
                    :content="marker.description"></MapPopup>
            </LPopup>
        </LMarker>
    </LMap>
</template>

<style>
.dark .leaflet-container {
    background: #171717;
}

.leaflet-container {
    background: #f4f4f4;
}

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

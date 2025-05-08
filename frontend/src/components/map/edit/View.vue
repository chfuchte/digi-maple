<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LControl, LImageOverlay, LMarker, LPopup, LIcon } from "@vue-leaflet/vue-leaflet";
import MapZoomButtons from "@/components/map/ZoomButtons.vue";
import { ref } from "vue";
import { latLngBounds, CRS, Map, LatLng } from "leaflet";
import { LucideMapPinPlus } from "lucide-vue-next";
import MapPin from "@/components/map/pins/index.vue";
import { Button } from "@/components/ui/button";
import MapPopup from "@/components/map/Popup.vue";
import type { MapPinType, Marker as MarkerType } from "@/typings/map";

type Marker = MarkerType & {
    id: number;
};

const props = defineProps<{
    mapImgUrl: string;
    mapImgWidth: number;
    mapImgHeight: number;
    markers?: Array<Marker>;
}>();

const emit = defineEmits<{
    leafletReady: [Map];
    createMarker: [void];
    markerClicked: [number];
    markerLocationUpdate: [number, LatLng];
}>();

const zoomInDisabled = ref(false);
const zoomOutDisabled = ref(true);
const zoomLevel = ref<number>(-2);

const leafletObject = ref<Map>();

const lastClickedMarker = ref<number | undefined>(undefined);

const onMapReady = (map: Map) => {
    leafletObject.value = map;
    emit("leafletReady", map);
    zoomLevel.value = map.getZoom();
};

const handleZoomEvent = (newZoomLevel: number) => {
    zoomLevel.value = newZoomLevel;
    zoomInDisabled.value = zoomLevel.value == leafletObject.value?.getMaxZoom();
    zoomOutDisabled.value = zoomLevel.value == leafletObject.value?.getMinZoom();
};

const markerClickedEvent = (id: number) => {
    lastClickedMarker.value = id;
    emit("markerClicked", id);
};

const markerLocationUpdatedEvent = (id: number, location: LatLng) => {
    emit("markerLocationUpdate", id, location);
};

const bounds = latLngBounds([0, 0], [2000, (props.mapImgWidth / props.mapImgHeight) * 2000]);
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
                :zoom-in-disabled="zoomInDisabled"
                :zoom-out-disabled="zoomOutDisabled" />
        </LControl>
        <LControl position="bottomright" class="flex rounded-md border bg-background p-1.5">
            <Button variant="secondary" @click="emit('createMarker')">
                <LucideMapPinPlus />
            </Button>
        </LControl>
        <LImageOverlay :url="props.mapImgUrl!" :bounds />
        <LMarker
            :key="marker.id"
            v-for="marker in markers"
            @click="() => markerClickedEvent(marker.id)"
            @update:lat-lng="(location: LatLng) => markerLocationUpdatedEvent(marker.id, location)"
            :draggable="true"
            :lat-lng="new LatLng(marker.y, marker.x)">
            <LIcon :iconSize="[32, 32]" class-name="border-none outline-none">
                <MapPin :variant="marker.icon as MapPinType" :style="{ color: marker.color }" :size="32" />
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

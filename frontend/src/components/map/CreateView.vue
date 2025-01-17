<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LControl, LImageOverlay, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import MapZoomButtons from "@/components/map/ZoomButtons.vue";
import { ref } from "vue";
import { latLngBounds, CRS, Map } from "leaflet";
import { LucideMapPinPlus } from "lucide-vue-next";
import { Button } from "@/components/ui/button";

const props = defineProps<{
    mapImgUrl: string;
    mapImgWidth: number;
    mapImgHeight: number;
    markers?: Array<{
        id: string;
        name?: string;
        lng: number;
        lat: number;
    }>;
}>();

const emit = defineEmits<{
    leafletReady: [Map];
    createMarker: [void];
    markerClicked: [string];
}>();

const zoomInDisabled = ref(false);
const zoomOutDisabled = ref(true);
const zoomLevel = ref<number>(-2);

const leafletObject = ref<Map>();

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

const markerClickedEvent = (id: string) => {
    emit("markerClicked", id);
};

const bounds = latLngBounds([0, 0], [props.mapImgWidth, props.mapImgHeight]);
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
        <LControl position="bottomright">
          <Button variant="outline" @click="emit('createMarker');">
            <LucideMapPinPlus/>
          </Button>
        </LControl>
        <LImageOverlay :url="props.mapImgUrl!" :bounds />
        <LMarker
            v-for="marker in markers"
            @click="markerClickedEvent(marker.id)"
            :draggable="true"
            :lat-lng="marker">
            <LPopup :content="marker.name" />
        </LMarker>
    </LMap>
</template>

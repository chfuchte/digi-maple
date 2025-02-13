<script setup lang="ts">
import { LIcon, LImageOverlay, LMap, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";

import type { MapMarker } from "@/schema/mapView.ts";
import { CRS, LatLng, latLngBounds, Map } from "leaflet";
import { ref, useTemplateRef, watch } from "vue";
import MapPopup from "@/components/map/Popup.vue";
import MapPin from "@/components/map/pins/index.vue";

const props = defineProps<{
    mapImgUrl: string;
    mapImgWidth: number;
    mapImgHeight: number;
    marker: MapMarker | null;
}>();

const leafletObject = ref<Map>();
const markerRef = useTemplateRef<InstanceType<typeof LMarker>>("marker");

const onMapReady = (map: Map) => {
    leafletObject.value = map;
};

const onPopupReady = () => {
    markerRef.value!.leafletObject?.openPopup();
};

const bounds = latLngBounds([0, 0], [props.mapImgWidth, props.mapImgHeight]);

watch(
    () => props.marker,
    (marker) => {
        if (marker != null) {
            leafletObject.value!.setView(new LatLng(marker.y + 12, marker.x), leafletObject.value!.getZoom());

            if (!markerRef.value!.leafletObject?.isPopupOpen()) {
                markerRef.value!.leafletObject?.openPopup();
            }
        }
    },
    { deep: true, flush: "post" },
);
</script>

<template>
    <LMap
        ref="preview"
        :zoom="1"
        :max-zoom="1"
        :min-zoom="-2"
        :crs="CRS.Simple"
        :center="[bounds.getCenter().lat, bounds.getCenter().lng]"
        :options="{
            zoomControl: false,
            attributionControl: false,
            dragging: false,
            scrollWheelZoom: 'center',
            doubleClickZoom: false,
        }"
        @ready="onMapReady">
        <LImageOverlay :url="props.mapImgUrl!" :bounds />
        <LMarker v-if="marker != null" ref="marker" :key="marker.id" :lat-lng="new LatLng(marker.y, marker.x)">
            <LIcon :iconSize="[32, 32]" class-name="border-none outline-none">
                <MapPin :variant="marker.display.icon" class="text-blue-600" :size="32" />
            </LIcon>
            <LPopup @ready="onPopupReady">
                <MapPopup
                    :title="marker.display.title"
                    :icon="marker.display.icon"
                    :content="marker.display.description">
                </MapPopup>
            </LPopup>
        </LMarker>
    </LMap>
</template>

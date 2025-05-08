<script setup lang="ts">
import { LIcon, LImageOverlay, LMap, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import { CRS, LatLng, latLngBounds, Map } from "leaflet";
import { ref, useTemplateRef, watch } from "vue";
import MapPopup from "@/components/map/Popup.vue";
import MapPin from "@/components/map/pins/index.vue";
import type { MapPinType, Marker } from "@/typings/map";

const props = defineProps<{
    mapImgUrl: string;
    mapImgWidth: number;
    mapImgHeight: number;
    marker: Marker | null;
}>();

const leafletObject = ref<Map>();
const markerRef = useTemplateRef<InstanceType<typeof LMarker>>("marker");

const onMapReady = (map: Map) => {
    leafletObject.value = map;
};

const onPopupReady = () => {
    markerRef.value!.leafletObject?.openPopup();
};

const bounds = latLngBounds([0, 0], [100, (props.mapImgWidth / props.mapImgHeight) * 100]);

watch(
    () => props.marker,
    (marker) => {
        if (marker != null) {
            leafletObject.value!.setView(
                new LatLng(bounds.getCenter().lat, bounds.getCenter().lng),
                leafletObject.value!.getZoom(),
            );

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
            scrollWheelZoom: false,
            doubleClickZoom: false,
        }"
        @ready="onMapReady">
        <LImageOverlay :url="props.mapImgUrl!" :bounds />
        <LMarker
            v-if="marker != null"
            ref="marker"
            :key="marker.id"
            :lat-lng="new LatLng(bounds.getCenter().lat, bounds.getCenter().lng)">
            <LIcon :iconSize="[32, 32]" class-name="border-none outline-none">
                <MapPin
                    :variant="marker.icon as MapPinType"
                    :style="{ color: marker.color }"
                    class="text-blue-600"
                    :size="32" />
            </LIcon>
            <LPopup @ready="onPopupReady">
                <MapPopup :title="marker.title" :icon="marker.icon as MapPinType" :content="marker.description">
                </MapPopup>
            </LPopup>
        </LMarker>
    </LMap>
</template>

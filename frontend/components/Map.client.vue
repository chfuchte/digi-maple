<script setup lang="ts">
import { ref } from "vue";
import { latLngBounds, CRS, Map } from "leaflet";

const props = defineProps<{
    image: string;
    name: string;
    width: number;
    height: number;
    markers?: Array<{
        name?: string;
        lng: number;
        lat: number;
    }>;
}>();

const zoomInDisabled = ref(false);
const zoomOutDisabled = ref(true);

let leafletObject = ref<Map | null>(null);

const onMapReady = (map: Map) => {
  leafletObject.value = map;
}

const zoomEvent = (zoomLevel: number) => {
  zoomInDisabled.value = zoomLevel == leafletObject.value?.getMaxZoom();
  zoomOutDisabled.value = zoomLevel == leafletObject.value?.getMinZoom();
}

const bounds = latLngBounds([0, 0], [props.width!, props.height!]);
</script>

<template>
    <div class="flex flex-col">
      <TitleBar>{{ props.name }}</TitleBar>
      <LMap
          ref="map"
          :zoom="-2"
          :center="[bounds.getCenter().lat, bounds.getCenter().lng]"
          :crs="CRS.Simple"
          :min-zoom="-2"
          :max-zoom="2"
          :options="{
                zoomControl: false,
                attributionControl: false,
            }"
          @ready="onMapReady"
          @update:zoom="zoomEvent"
          class="flex-grow">
        <LControl position="bottomleft">
          <MapZoom
              @zoom-in="leafletObject?.zoomIn();"
              @zoom-out="leafletObject?.zoomOut();"
              :disable-zoom-in="zoomInDisabled"
              :disable-zoom-out="zoomOutDisabled"
          />
        </LControl>
        <LImageOverlay :url="props.image!" :bounds />
        <LMarker v-for="marker in markers" :key="marker.name ?? ''" :lat-lng="marker">
          <LPopup :content="marker.name ?? ''" />
        </LMarker>
      </LMap>
    </div>
</template>
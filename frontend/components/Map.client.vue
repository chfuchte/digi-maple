<script setup lang="ts">
import { ref } from "vue";
import { latLngBounds, CRS } from "leaflet";

const props = defineProps<{
    image: string;
    width: number;
    height: number;
    markers?: Array<{
        name?: string;
        lng: number;
        lat: number;
    }>;
}>();

const zoom = ref(-2);

const bounds = latLngBounds([0, 0], [props.width!, props.height!]);
</script>

<template>
    <div style="height: 100vh; width: 100vw">
        <LMap
            ref="map"
            :zoom="zoom"
            :center="[bounds.getCenter().lat, bounds.getCenter().lng]"
            :crs="CRS.Simple"
            :min-zoom="-2"
            :max-zoom="2">
            <LImageOverlay :url="props.image!" :bounds />
            <LMarker v-for="marker in markers" :key="marker.name ?? ''" :lat-lng="marker">
                <LPopup :content="marker.name ?? ''" />
            </LMarker>
            <!--<LMarker
          :lat-lng="bounds.getCenter()"
          title="Ich bin die Mitte"
      />-->
        </LMap>
    </div>
</template>

<style scoped></style>

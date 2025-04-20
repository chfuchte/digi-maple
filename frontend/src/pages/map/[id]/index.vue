<script setup lang="ts">
import { apiGetMap } from '@/queries/maps';
import type { FullMap } from '@/typings/map';
import { onBeforeMount, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import MapView from "@/components/map/View.vue";
import Layout from "@/components/layouts/default.vue";

const route = useRoute();
const router = useRouter();

const map = ref<FullMap | null>(null);

onBeforeMount(async () => {
    const mapId = route.params.id as string;

    if (isNaN(Number(mapId))) {
        await router.push("/");
        return;
    }

    const mapRes = await apiGetMap(parseInt(mapId));

    if (!mapRes) {
        await router.push("/");
        return;
    }

    map.value = mapRes;
});

</script>

<template>
    <Layout>
        <MapView v-if="map" :map-img-url="map.imgUrl" :map-img-width="map.imgWidth" :map-imgheight="map.imgHeight"
            :markers="map.markers" />
    </Layout>
</template>
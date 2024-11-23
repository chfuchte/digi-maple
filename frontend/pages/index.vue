<script setup lang="ts">
import devMapImagePath from "@/assets/dev/Lageplan_Campus_Bockenheim.svg";

const imageHeightWidthRatio = 0.94285675588;
const height = 2000;
const width = imageHeightWidthRatio * height;
</script>

<template>
    <Map
        :image="devMapImagePath"
        :width="width"
        :height="height"
        :markers="[
            {
                name: 'Test',
                lng: width / 2,
                lat: height / 2,
            },
        ]" />
</template>

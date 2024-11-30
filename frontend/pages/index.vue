<script setup lang="ts">
import devMapImagePath from "@/assets/dev/Lageplan_Campus_Bockenheim.svg";

const imageHeightWidthRatio = 0.94285675588;
const height = 2000;
const width = imageHeightWidthRatio * height;
</script>

<template>
    <div class="flex flex-col w-screen h-screen">
        <DebugBar />
        <Map
            :image="devMapImagePath"
            name="Uni Campus Bockenheim"
            :width="width"
            :height="height"
            :markers="[
            {
                name: 'Test',
                lng: width / 2,
                lat: height / 2,
            },
        ]"
            class="flex-grow"
        />
    </div>
</template>

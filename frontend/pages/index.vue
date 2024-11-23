<script setup lang="ts">
import polandMap from "@/assets/big_poland_with_districts.png";
</script>

<template>
    <Map
        :image="polandMap"
        :width="2049"
        :height="2108"
        :markers="[
            {
                name: 'Test',
                lng: 2049 / 2,
                lat: 2108 / 2,
            },
        ]" />
</template>

<script setup lang="ts">
import WheelchairPin from "@/components/map/pins/wheelchair.vue";
import DefaultPin from "@/components/map/pins/default.vue";
import InfoPin from "@/components/map/pins/info.vue";
import WarningPin from "@/components/map/pins/warning.vue";
import type { MapPinType } from "@/typings/map";

const props = defineProps<{
    size?: number;
    variant?: MapPinType;
}>();
</script>

<template>
    <WheelchairPin v-if="props.variant == 'wheelchair'" :size="props.size" />
    <WarningPin v-else-if="props.variant == 'warning'" :size="props.size" />
    <InfoPin v-else-if="props.variant == 'info'" :size="props.size" />
    <DefaultPin v-else :size="props.size" />
</template>

<script setup lang="ts">
import WheelchairPin from "@/components/map/pins/wheelchair.vue";
import DefaultPin from "@/components/map/pins/default.vue";
import InfoPin from "@/components/map/pins/info.vue";
import WarningPin from "@/components/map/pins/warning.vue";
import type { MapPinType } from "@/typings/map";
import ElevatorPin from "./elevator.vue";
import StairsPin from "./stairs.vue";
import BusPin from "./bus.vue";
import CarPin from "./car.vue";
import BikePin from "./bike.vue";

const props = defineProps<{
    size?: number;
    variant?: MapPinType;
}>();
</script>

<template>
    <WheelchairPin v-if="props.variant == 'wheelchair'" :size="props.size" />
    <WarningPin v-else-if="props.variant == 'warning'" :size="props.size" />
    <InfoPin v-else-if="props.variant == 'info'" :size="props.size" />
    <ElevatorPin v-else-if="props.variant == 'elevator'" :size="props.size" />
    <StairsPin v-else-if="props.variant == 'stairs'" :size="props.size" />
    <BusPin v-else-if="props.variant == 'bus'" :size="props.size" />
    <CarPin v-else-if="props.variant == 'car'" :size="props.size" />
    <BikePin v-else-if="props.variant == 'bike'" :size="props.size" />
    <DefaultPin v-else :size="props.size" />
</template>

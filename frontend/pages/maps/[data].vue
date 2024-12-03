<script setup lang="ts">
import devMapImagePath from "@/assets/dev/Lageplan_Campus_Bockenheim.svg";

/*const imageHeightWidthRatio = 0.94285675588;
const height = 2000;
const width = imageHeightWidthRatio * height;*/

definePageMeta({
    validate: async (route) => {
        function base64ToBytes(base64: string): Uint8Array {
            const binString = atob(base64);
            return Uint8Array.from(binString, (m) => m.codePointAt(0)!);
        }

        try {
            JSON.parse(new TextDecoder().decode(base64ToBytes(route.params.data as string)));
            return true;
        } catch (e) {
            return { "statusCode": 400, "statusMessage": "Invalid data" };
        }
    },
});

const route = useRoute()

function base64ToBytes(base64: string): Uint8Array {
    const binString = atob(base64);
    return Uint8Array.from(binString, (m) => m.codePointAt(0)!);
}

const data: {
    name: string,
    width: number,
    height: number,
    markers: { name: string, lng: number, lat: number }[]
} = JSON.parse(new TextDecoder().decode(base64ToBytes(route.params.data as string)));
</script>

<template>
    <div class="flex flex-col flex-grow">
        <TitleHeader :title="data.name"></TitleHeader>
        <MapView
            :image="devMapImagePath"
            :width="data.width"
            :height="data.height"
            :markers="data.markers"
        />
    </div>
</template>

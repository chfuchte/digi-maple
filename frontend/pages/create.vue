<script setup lang="ts">
import devMapImagePath from "@/assets/dev/Lageplan_Campus_Bockenheim.svg";
import { ref } from "vue";
import { Map } from "leaflet";
import type { Marker } from "leaflet";
import { DialogDescription } from "~/components/ui/dialog";

let leafletObject: Map | null = null;

let markers = ref<{id: string, lng: number, lat: number}[]>([
    {"id": crypto.randomUUID(), "lng": 2000 / 2, "lat": 1885.71351176 / 2}
]);

function onMapReady(map: Map) {
    leafletObject = map;
}

function add() {
    markers.value.push({"id": crypto.randomUUID(), "lng": leafletObject!.getCenter().lng, "lat": leafletObject!.getCenter().lat });
}

function bytesToBase64(bytes: Uint8Array): string {
    const binString = Array.from(bytes, (byte) =>
        String.fromCodePoint(byte),
    ).join("");
    return btoa(binString);
}

function generate() {
    const markers = <{name: string, lng: number, lat: number}[]>[]
    leafletObject!.eachLayer((layer) => {
        // We can't test if it's an instance of Marker because it's not available in a universal-render page.
        // So we use this workaround.
        // We also can't use refs on the LMarkers because their API is incomplete.
        if (layer.options.hasOwnProperty("draggable")) {
            const marker = layer as Marker;
            markers.push({"name": marker.getAttribution!() as string, "lng": marker.getLatLng().lng, "lat": marker.getLatLng().lat});
        }
    });

    const data = {
        "name": crypto.randomUUID(),
        "width": 1885.71351176,
        "height": 2000,
        "markers": markers
    };

    return bytesToBase64(new TextEncoder().encode(JSON.stringify(data)))
}
</script>

<template>
    <TitleHeader title="Creating Map">
        <Dialog>
            <DialogTrigger>
                <Button variant="secondary">Generate</Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>
                        Generated data string
                    </DialogTitle>
                    <DialogDescription>
                        This is your Base64 encoded data string!
                    </DialogDescription>
                </DialogHeader>
                <div>
                    <p class="break-all whitespace-normal">{{ generate() }}</p>
                </div>
                <DialogFooter>
                    <Button @click="navigateTo(`/maps/${generate()}`, { open: { target: '_blank' } })">
                        Open
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </TitleHeader>
    <aside class="absolute right-0 bottom-0 p-1.5">
        <Button variant="outline" size="icon" @click="add">
            <LucideCirclePlus class="w-20 h-20"></LucideCirclePlus>
        </Button>
    </aside>
    <MapView
        :image="devMapImagePath"
        :width="1885.71351176"
        :height="2000"
        @onMapReady="onMapReady"
        class="flex-grow"
    >
        <LMarker :draggable="true" v-for="marker in markers" :lat-lng="marker" :attribution="marker.id">
            <LPopup :content="marker.id" />
        </LMarker>
    </MapView>
</template>

<style scoped>
aside {
    z-index: 500;
}
</style>
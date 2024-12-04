<script setup lang="ts">
import devMapImagePath from "@/assets/dev/Lageplan_Campus_Bockenheim.svg";
import { ref } from "vue";
import { Map } from "leaflet";
import type { Marker } from "leaflet";

interface IMarker {
    id: string;
    name: string;
    lng: number;
    lat: number;
}

let createdMarkers = ref<IMarker[]>([
    { id: crypto.randomUUID(), name: "Test 1", lng: 2000 / 2, lat: 1885.71351176 / 2 },
]);
let title = "";

let leafletObject: Map | null = null;

let markerNameModel = defineModel<string>("markerNameModel");
let titleModel = defineModel<string>("titleModel");

function onMapReady(map: Map): void {
    leafletObject = map;
}

function addMarker(name: string): void {
    createdMarkers.value.push({
        id: crypto.randomUUID(),
        name: name,
        lng: leafletObject!.getCenter().lng,
        lat: leafletObject!.getCenter().lat,
    });
}

function bytesToBase64(bytes: Uint8Array): string {
    const binString = Array.from(bytes, (byte) => String.fromCodePoint(byte)).join("");
    return btoa(binString);
}

function generate(): string {
    const markers = <IMarker[]>[];
    leafletObject!.eachLayer((layer) => {
        // We can't test if it's an instance of Marker because it's not available in a universal-render page.
        // So we use this workaround.
        // We also can't use refs on the LMarkers because their API is incomplete.
        if (layer.options.hasOwnProperty("draggable")) {
            const marker = layer as Marker;
            const id = marker.getAttribution!() as string;
            markers.push({
                id: id,
                name: createdMarkers.value.find((current) => current.id == id)?.name ?? "Something went wrong!",
                lng: marker.getLatLng().lng,
                lat: marker.getLatLng().lat,
            });
        }
    });

    const data = {
        name: title,
        width: 1885.71351176,
        height: 2000,
        markers: markers,
    };

    return bytesToBase64(new TextEncoder().encode(JSON.stringify(data)));
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
                    <DialogTitle> Generated data string </DialogTitle>
                    <DialogDescription> This is your Base64 encoded data string! </DialogDescription>
                </DialogHeader>
                <div class="max-h-96 overflow-y-auto">
                    <pre class="whitespace-normal break-all">{{ generate() }}</pre>
                </div>
                <DialogFooter>
                    <Button @click="navigateTo(`/maps/${generate()}`, { open: { target: '_blank' } })"> Open </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </TitleHeader>
    <div class="over-map absolute right-0 top-24 overflow-hidden">
        <Drawer title="Title">
            <div
                class="flex flex-col items-start rounded-bl border-b border-l border-t border-black bg-white p-3.5 text-black">
                <h1 class="font-bold">Map title</h1>
                <h3 class="text-sm text-gray-700">Enter a short title.</h3>
                <Input v-model:model-value="titleModel" class="mt-2" type="text" placeholder="Title"></Input>
                <Button variant="secondary" class="mt-2 self-end" @click="title = titleModel!">Save</Button>
            </div>
        </Drawer>
    </div>
    <div class="over-map absolute bottom-0 right-0 p-1.5">
        <Dialog>
            <DialogTrigger>
                <Button variant="outline" size="icon">
                    <LucideCirclePlus class="h-20 w-20"></LucideCirclePlus>
                </Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle> Add marker </DialogTitle>
                    <DialogDescription> Enter a name. </DialogDescription>
                </DialogHeader>
                <Input v-model:model-value="markerNameModel" type="text" placeholder="Name" />
                <DialogFooter>
                    <DialogClose>
                        <Button @click="addMarker(markerNameModel!)"> Create </Button>
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
    <MapView :image="devMapImagePath" :width="1885.71351176" :height="2000" @onMapReady="onMapReady" class="flex-grow">
        <LMarker :draggable="true" v-for="marker in createdMarkers" :lat-lng="marker" :attribution="marker.id">
            <LPopup :content="marker.name" />
        </LMarker>
    </MapView>
</template>

<style scoped>
.over-map {
    z-index: 500;
}
</style>

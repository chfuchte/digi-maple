<script setup lang="ts">
import devMapImagePath from "@/assets/dev/Lageplan_Campus_Bockenheim.svg";
import { ref } from "vue";
import { Map } from "leaflet";

definePageMeta({
    middleware: 'auth'
});

const imageHeightWidthRatio = 0.94285675588;
const height = 2000;
const width = imageHeightWidthRatio * height;

interface IMarker {
    name: string;
    lng: number;
    lat: number;
}

let leafletObject: Map | null = null;

let markerNameModel = defineModel<string>("markerNameModel");
let titleModel = defineModel<string>("titleModel");
let markers = ref<Array<IMarker>>([]);
let title = ref("Neue Karte");

useHead({
    title: title,
});

function onMapReady(map: Map): void {
    leafletObject = map;
}

function addMarker(name: string): void {
    markers.value.push({
        name: name,
        lng: leafletObject!.getCenter().lng,
        lat: leafletObject!.getCenter().lat,
    });
}

/*
old code
function generate() {
    const markers = <IMarker[]>[];
    leafletObject!.eachLayer((layer) => {
        // We can't test if it's an instance of Marker because it's not available in a universal-render page.
        // So we use this workaround.
        // We also can't use refs on the LMarkers because their API is incomplete.
        if (layer.options.hasOwnProperty("draggable")) {
            const marker = layer as Marker;
            const id = marker.getAttribution!() as string;
            markers.push({
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

    return data;
}
*/
</script>

<template>
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
    <MapCreateView
        @leaflet-ready="onMapReady"
        :map-img-url="devMapImagePath"
        :map-img-width="width"
        :map-imgheight="height"
        :markers="markers" />
</template>

<style scoped>
.over-map {
    z-index: 500;
}
</style>

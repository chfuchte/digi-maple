<script setup lang="ts">
import { ref } from "vue";
import { type LatLng, Map } from "leaflet";
import { useHead } from "@unhead/vue";
import Layout from "@/components/layouts/default.vue";
import MapCreateView from "@/components/map/edit/View.vue";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

import { type MapMarker, markerTypes } from "@/schema/mapView";
import { LucideAccessibility, LucideAlertTriangle, LucideInfo, LucidePin } from "lucide-vue-next";

const devMapImagePath = "dev/Lageplan_Campus_Bockenheim.svg";
const imageHeightWidthRatio = 0.94285675588;
const height = 2000;
const width = imageHeightWidthRatio * height;

let leafletObject: Map | null = null;

const selectedMarker = ref<number | null>();

const markers = ref<Array<MapMarker>>([]);
const title = ref("Neue Karte");
const description = ref("");

const markerNameModel = defineModel<string>("markerNameModel");
const markerDescriptionModel = defineModel<string>("markerDescriptionModel");
const markerTypeModel = defineModel<MapMarker["display"]["icon"]>("typeModel");

const markerColorModel = defineModel<string>("markerColorModel");
markerColorModel.value = "#2563eb";

const descriptionModel = defineModel<string>("descriptionModel");
descriptionModel.value = description.value;

const titleModel = defineModel<string>("titleModel");
titleModel.value = title.value;

useHead({
    title: title,
});

function onMapReady(map: Map): void {
    leafletObject = map;
}

function createMarker(): void {
    markers.value.push({
        id: crypto.randomUUID(),
        x: leafletObject!.getCenter().lng,
        y: leafletObject!.getCenter().lat,
        display: {
            title: "Marker",
            description: "Lorem Ipsum.....",
            icon: "default",
            color: "#2563eb",
        },
    });
}

function deleteMarker(): void {
    markers.value = markers.value.filter((_, index) => index !== selectedMarker.value!);
    selectedMarker.value = null;
    markerNameModel.value = "";
    markerDescriptionModel.value = "";
    markerTypeModel.value = undefined;
    markerColorModel.value = "#2563eb";
}

function editMarker(): void {
    markers.value[selectedMarker.value!].display.description = markerDescriptionModel.value!;
    markers.value[selectedMarker.value!].display.title = markerNameModel.value!;
    markers.value[selectedMarker.value!].display.icon = markerTypeModel.value!;
    markers.value[selectedMarker.value!].display.color = markerColorModel.value!;
}

function markerClicked(id: string): void {
    const marker = markers.value.findIndex((marker) => marker.id == id);
    selectedMarker.value = marker;
    markerNameModel.value = markers.value[marker].display.title;
    markerDescriptionModel.value = markers.value[marker].display.description;
    markerTypeModel.value = markers.value[marker].display.icon;
    markerColorModel.value = markers.value[marker].display.color;
}

function markerLocationUpdated(id: string, location: LatLng): void {
    const marker = markers.value.findIndex((marker) => marker.id == id);

    markers.value[marker].x = location.lng;
    markers.value[marker].y = location.lat;
}
</script>

<template>
    <Layout>
        <ResizablePanelGroup direction="horizontal">
            <ResizablePanel :min-size="22" :default-size="30" :max-size="75" class="w-1/3">
                <aside class="[&::scrollbar-width]:[thin] h-full overflow-y-auto p-4">
                    <form class="flex w-full flex-col items-start gap-6">
                        <fieldset class="flex w-full flex-col gap-6 rounded-lg border p-4">
                            <legend class="-ml-1 px-1 text-sm font-medium">Settings</legend>
                            <div class="flex flex-col gap-3">
                                <Label for="name">Name</Label>
                                <Input
                                    v-model:model-value="titleModel"
                                    id="name"
                                    type="text"
                                    placeholder="Campus Bockenheim"
                                    autocomplete="off" />
                                <Label for="description">Description</Label>
                                <Textarea
                                    v-model:model-value="descriptionModel"
                                    id="description"
                                    type="text"
                                    placeholder="Eine Karte mit verschiedenen Markern." />
                                <Button
                                    @click="
                                        title = titleModel!;
                                        description = descriptionModel!;
                                    "
                                    variant="secondary"
                                    type="button"
                                    :disabled="title == titleModel && description == descriptionModel">
                                    Speichern
                                </Button>
                            </div>
                        </fieldset>
                        <fieldset
                            class="flex w-full flex-col gap-6 rounded-lg border p-4"
                            :disabled="selectedMarker == null">
                            <legend class="-ml-1 px-1 text-sm font-medium">Edit marker</legend>
                            <div class="flex flex-col gap-3">
                                <Label for="name">Name</Label>
                                <Input
                                    v-model:model-value="markerNameModel"
                                    id="name"
                                    type="text"
                                    autocomplete="off"
                                    placeholder="Gebäude B" />
                                <Label for="description">Description</Label>
                                <Textarea
                                    v-model:model-value="markerDescriptionModel"
                                    id="description"
                                    type="text"
                                    placeholder="Aufzüge sind kapput!" />
                                <Label for="type">Type</Label>
                                <div class="flex gap-3">
                                    <Select id="type" v-model:model-value="markerTypeModel" class="flex">
                                        <SelectTrigger class="w-full" :disabled="selectedMarker == null">
                                            <SelectValue placeholder="Select a type" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectGroup>
                                                <SelectLabel>Marker Typ</SelectLabel>
                                                <SelectItem v-for="icon in markerTypes" :value="icon" :key="icon">
                                                    <div class="flex flex-row items-center gap-2">
                                                        <LucideAccessibility v-if="icon == 'weelchair'" :size="18" />
                                                        <LucideAlertTriangle v-else-if="icon == 'warning'" :size="18" />
                                                        <LucideInfo v-else-if="icon == 'info'" :size="18" />
                                                        <LucidePin v-else :size="18" />

                                                        {{ icon }}
                                                    </div>
                                                </SelectItem>
                                            </SelectGroup>
                                        </SelectContent>
                                    </Select>
                                    <Input
                                        v-model:model-value="markerColorModel"
                                        id="color"
                                        type="color"
                                        autocomplete="off"
                                        class="max-w-[250px]" />
                                </div>
                                <Button
                                    variant="destructive"
                                    @click="deleteMarker()"
                                    type="button"
                                    :disabled="selectedMarker == null">
                                    Löschen
                                </Button>
                                <Button
                                    variant="secondary"
                                    @click="editMarker()"
                                    type="button"
                                    :disabled="
                                        selectedMarker != null &&
                                        markers[selectedMarker].display.title == markerNameModel &&
                                        markers[selectedMarker].display.description == markerDescriptionModel &&
                                        markers[selectedMarker].display.icon == markerTypeModel &&
                                        markers[selectedMarker].display.color == markerColorModel
                                    ">
                                    Ändern
                                </Button>
                            </div>
                        </fieldset>
                    </form>
                </aside>
            </ResizablePanel>
            <ResizableHandle with-handle />
            <ResizablePanel>
                <MapCreateView
                    @leaflet-ready="onMapReady"
                    @create-marker="createMarker"
                    @marker-clicked="markerClicked"
                    @marker-location-update="markerLocationUpdated"
                    :map-img-url="devMapImagePath"
                    :map-img-width="width"
                    :map-img-height="height"
                    :markers="markers" />
            </ResizablePanel>
        </ResizablePanelGroup>
    </Layout>
</template>

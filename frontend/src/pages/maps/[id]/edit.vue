<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import { onBeforeMount, ref, watch } from "vue";
import type { FullMap as ApiMap, MapPinType, Marker } from "@/typings/map";
import { useRouter, useRoute } from "vue-router";
import {
    apiAddMarker,
    apiDeleteMarker,
    apiGetMap,
    apiUpdateMap,
    apiUpdateMarker,
    apiUploadMapImg,
} from "@/queries/maps";
import type { LatLng, Map } from "leaflet";
import Label from "@/components/ui/label/Label.vue";
import { Input as UInput } from "@/components/ui/input";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import Preview from "@/components/map/edit/Preview.vue";
import View from "@/components/map/edit/View.vue";
import { Textarea } from "@/components/ui/textarea";
import { LucideAccessibility, LucideAlertTriangle, LucideInfo, LucidePin } from "lucide-vue-next";
import { toast } from "vue-sonner";

const router = useRouter();
const route = useRoute();
const map = ref<ApiMap | null>(null);

onBeforeMount(async () => {
    const mapId = route.params.id as string;

    if (isNaN(Number(mapId))) {
        await router.push("/dashboard");
        return;
    }

    const mapRes = await apiGetMap(parseInt(mapId));

    if (!mapRes) {
        await router.push("/dashboard");
        return;
    }

    map.value = mapRes;
    title.value = mapRes.name;
    file.value = null;
});

let leafletObject: Map | null = null;
const file = ref<File | null>(null);
const title = ref("Neue Karte");

const selectedMarker = ref<Marker["id"] | null>(null);
const selectedMarkerEdits = ref<Omit<Marker, "id">>({
    title: "",
    description: "",
    color: "#2563eb",
    icon: "default",
    x: 0,
    y: 0,
});

const didMarkerChange = ref<boolean>(false);

watch(
    selectedMarkerEdits,
    async (newEdits) => {
        didMarkerChange.value = checkForMarkerChange(newEdits);
    },
    { deep: true },
);

function checkForMarkerChange(newMarker: Omit<Marker, "id">): boolean {
    if (!map.value || !selectedMarkerEdits.value) return false;

    const marker = map.value.markers[selectedMarker.value!];
    if (marker.color == newMarker.color) return false;
    return true;
}

function onMapReady(map: Map): void {
    leafletObject = map;
}

async function setMapTitle() {
    if (!title.value || !map.value) return;

    const mapUpdateResult = await apiUpdateMap(map.value.id, title.value);
    if (!mapUpdateResult) {
        toast.error("Fehler beim Aktualisieren des Kartennamens.", {
            description: "Bitte versuche es später erneut.",
        });
        return;
    }

    map.value.name = title.value;
    toast.success("Kartennamen erfolgreich aktualisiert.");
}

async function uploadMapImage() {
    if (!file.value || !map.value) return;

    const mapUpdateResult = await apiUploadMapImg(file.value, map.value.id);
    if (!mapUpdateResult) {
        toast.error("Fehler beim Hochladen des Kartenbildes.", {
            description: "Bitte versuche es später erneut.",
        });
        return;
    }

    const mapRes = await apiGetMap(map.value.id);

    if (!mapRes) {
        await router.push("/dashboard");
        return;
    }

    map.value = mapRes;
    title.value = mapRes.name;
    file.value = null;

    toast.success("Kartenbild erfolgreich hochgeladen.");
}

async function createMarker() {
    if (!leafletObject || !map.value) return;

    const res = await apiAddMarker(
        map.value.id,
        leafletObject!.getCenter().lng,
        leafletObject!.getCenter().lat,
        "Neuer Marker",
        "",
        "default",
        "#2563eb",
    );
    if (!res) {
        toast.error("Fehler beim Erstellen des Markers.", {
            description: "Bitte versuche es später erneut.",
        });
        return;
    }

    map.value.markers.push({
        id: res.id,
        x: leafletObject!.getCenter().lng,
        y: leafletObject!.getCenter().lat,
        title: "Neuer Marker",
        description: "",
        icon: "default",
        color: "#2563eb",
    });

    markerClicked(map.value.markers[map.value.markers.length - 1].id);
    toast.success("Marker hinzugefügt");
}

function markerClicked(id: number): void {
    const marker = map.value!.markers.findIndex((marker) => marker.id == id);
    selectedMarker.value = marker;
    selectedMarkerEdits.value = {
        title: map.value!.markers[marker].title,
        description: map.value!.markers[marker].description,
        icon: map.value!.markers[marker].icon as MapPinType,
        color: map.value!.markers[marker].color,
        x: map.value!.markers[marker].x,
        y: map.value!.markers[marker].y,
    };
    didMarkerChange.value = checkForMarkerChange(selectedMarkerEdits.value);
}

async function markerLocationUpdated(id: number, location: LatLng) {
    const marker = map.value!.markers.findIndex((marker) => marker.id == id);

    if (selectedMarker.value != marker) {
        markerClicked(id);
    }

    const res = await apiUpdateMarker(map.value!.id, id, {
        x: location.lng,
        y: location.lat,
    });

    if (!res) {
        toast.error("Fehler beim Aktualisieren des Markers.", {
            description: "Bitte versuche es später erneut.",
        });
        // move marker back to old location
        map.value!.markers[marker].x = map.value!.markers[marker].x;
        map.value!.markers[marker].y = map.value!.markers[marker].y;
        return;
    }

    map.value!.markers[marker].x = location.lng;
    map.value!.markers[marker].y = location.lat;
}

async function saveChangesOfSelectMarker() {
    if (!map.value || !selectedMarkerEdits.value) return;

    const marker = map.value.markers[selectedMarker.value!];

    const res = await apiUpdateMarker(map.value.id, marker.id, {
        title: selectedMarkerEdits.value.title,
        description: selectedMarkerEdits.value.description,
        icon: selectedMarkerEdits.value.icon,
        color: selectedMarkerEdits.value.color,
    });

    if (!res) {
        toast.error("Fehler beim Aktualisieren des Markers.", {
            description: "Bitte versuche es später erneut.",
        });
        return;
    }

    map.value.markers[selectedMarker.value!].title = selectedMarkerEdits.value.title;
    map.value.markers[selectedMarker.value!].description = selectedMarkerEdits.value.description;
    map.value.markers[selectedMarker.value!].icon = selectedMarkerEdits.value.icon;
    map.value.markers[selectedMarker.value!].color = selectedMarkerEdits.value.color;
    toast.success("Marker erfolgreich aktualisiert.");

    didMarkerChange.value = false;
}

async function deleteSelectedMarker() {
    if (!map.value || selectedMarker.value == null) return;

    const marker = map.value.markers[selectedMarker.value!];

    const res = await apiDeleteMarker(map.value.id, marker.id);

    if (!res) {
        toast.error("Fehler beim Löschen des Markers.", {
            description: "Bitte versuche es später erneut.",
        });
        return;
    }

    map.value.markers.splice(selectedMarker.value!, 1);
    selectedMarker.value = null;
    selectedMarkerEdits.value = {
        title: "",
        description: "",
        color: "#2563eb",
        icon: "default",
        x: 0,
        y: 0,
    };
    toast.success("Marker erfolgreich gelöscht.");
}
</script>

<template>
    <Layout>
        <ResizablePanelGroup direction="horizontal">
            <ResizablePanel :min-size="22" :default-size="30" :max-size="75" class="w-1/3">
                <aside class="[&::scrollbar-width]:[thin] h-full overflow-y-auto p-4">
                    <div class="flex w-full flex-col items-start gap-6">
                        <fieldset class="flex w-full flex-col gap-6 rounded-lg border p-4">
                            <legend class="-ml-1 px-1 text-sm font-medium">Generelles</legend>
                            <div class="flex flex-col gap-3">
                                <Label for="name">Name</Label>
                                <UInput
                                    v-model="title"
                                    id="name"
                                    type="text"
                                    placeholder="Campus Bockenheim"
                                    autocomplete="off" />
                                <Button variant="secondary" type="button" @click="setMapTitle"> Speichern </Button>
                            </div>
                            <div class="flex flex-col gap-3">
                                <Label for="file">Kartenbild</Label>
                                <input
                                    type="file"
                                    accept="image/*"
                                    @input="(event: any) => (file = event.target.files[0])" />
                                <Button variant="secondary" type="button" @click="uploadMapImage"> Hochladen </Button>
                            </div>
                        </fieldset>
                        <fieldset class="flex w-full flex-col gap-6 rounded-lg border p-4">
                            <legend class="-ml-1 px-1 text-sm font-medium">Ausgewählten Marker bearbeiten</legend>
                            <div class="h-[150px] w-full" v-if="map && map.imgUrl && map.imgWidth && map.imgHeight">
                                <Preview
                                    :map-img-url="map.imgUrl"
                                    :map-img-width="map.imgWidth"
                                    :map-img-height="map.imgHeight"
                                    :marker="
                                        selectedMarker != null ? { id: selectedMarker, ...selectedMarkerEdits } : null
                                    "
                                    class="rounded-md" />
                            </div>
                            <div class="flex flex-col gap-3">
                                <Label for="name">Name</Label>
                                <UInput
                                    v-model="selectedMarkerEdits.title"
                                    id="name"
                                    type="text"
                                    autocomplete="off"
                                    placeholder="Gebäude B" />
                                <Label for="description">Beschreibung</Label>
                                <Textarea
                                    v-model="selectedMarkerEdits.description"
                                    id="description"
                                    type="text"
                                    placeholder="Aufzüge sind kapput!" />
                                <Label for="type">Stil</Label>
                                <div class="flex gap-3">
                                    <Select v-model:model-value="selectedMarkerEdits.icon" id="type" class="flex">
                                        <SelectTrigger class="w-full">
                                            <SelectValue placeholder="Select a type" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectGroup>
                                                <SelectLabel>Marker Typ</SelectLabel>
                                                <SelectItem
                                                    v-for="icon in ['default', 'info', 'wheelchair', 'warning']"
                                                    :value="icon"
                                                    :key="icon">
                                                    <div class="flex flex-row items-center gap-2">
                                                        <LucideAccessibility v-if="icon == 'wheelchair'" :size="18" />
                                                        <LucideAlertTriangle v-else-if="icon == 'warning'" :size="18" />
                                                        <LucideInfo v-else-if="icon == 'info'" :size="18" />
                                                        <LucidePin v-else :size="18" />
                                                        {{ icon }}
                                                    </div>
                                                </SelectItem>
                                            </SelectGroup>
                                        </SelectContent>
                                    </Select>
                                    <UInput
                                        v-model="selectedMarkerEdits.color"
                                        id="color"
                                        type="color"
                                        autocomplete="off"
                                        class="max-w-[250px]" />
                                </div>
                                <Button @click="deleteSelectedMarker" variant="destructive" type="button">
                                    Löschen
                                </Button>
                                <Button
                                    @click="saveChangesOfSelectMarker"
                                    :disabled="!didMarkerChange"
                                    variant="secondary"
                                    type="button">
                                    Übernehmen
                                </Button>
                            </div>
                        </fieldset>
                    </div>
                </aside>
            </ResizablePanel>
            <ResizableHandle with-handle />
            <ResizablePanel>
                <View
                    v-if="map && map.imgHeight && map.imgWidth"
                    @leaflet-ready="onMapReady"
                    @create-marker="createMarker"
                    @marker-clicked="markerClicked"
                    @marker-location-update="markerLocationUpdated"
                    :map-img-url="map.imgUrl"
                    :map-img-width="map.imgWidth!"
                    :map-img-height="map.imgHeight!"
                    :markers="map.markers" />
                <div v-else class="flex h-full w-full items-center justify-center">
                    <p class="text-center text-3xl font-semibold">Kein Kartenbild gefunden</p>
                </div>
            </ResizablePanel>
        </ResizablePanelGroup>
    </Layout>
</template>

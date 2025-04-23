<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import { onBeforeMount, ref } from "vue";
import type { FullMap as ApiMap, MapPinType, Marker } from "@/typings/map";
import { useRouter, useRoute } from "vue-router";
import { apiGetMap, apiUpdateMap, apiUploadMapImg } from "@/queries/maps";
import type { Map } from "leaflet";
import Label from "@/components/ui/label/Label.vue";
import { Input as UInput } from "@/components/ui/input";
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import Preview from "@/components/map/edit/Preview.vue";
import View from "@/components/map/edit/View.vue";
import { Textarea } from "@/components/ui/textarea";
import { LucideAccessibility, LucideAlertTriangle, LucideInfo, LucidePin } from "lucide-vue-next";


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
const selectedMarkerEdits = ref<{
    name: string;
    description: string;
    type: MapPinType;
    color: string;
    icon: string;
    x: number;
    y: number;
}>();


function onMapReady(map: Map): void {
    leafletObject = map;
}

async function setMapTitle() {
    if (!title.value || !map.value) return;

    const mapUpdateResult = await apiUpdateMap(map.value.id, title.value);
    if (!mapUpdateResult) {
        alert("Failed to update map title");
        return;
    }

    map.value.name = title.value;
}

async function uploadMapImage() {
    if (!file.value || !map.value) return;

    const mapUpdateResult = await apiUploadMapImg(file.value, map.value.id);
    if (!mapUpdateResult) {
        alert("Failed to update map image");
        return;
    }
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
                                <UInput v-model="title" id="name" type="text" placeholder="Campus Bockenheim" autocomplete="off" />
                                <Button variant="secondary" type="button" @click="setMapTitle">
                                    Speichern
                                </Button>
                            </div>
                            <div class="flex flex-col gap-3">
                                <Label for="file">Kartenbild</Label>
                                <input type="file" accept="image/*"
                                    @input="(event: any) => (file = event.target.files[0])" />
                                <Button variant="secondary" type="button" @click="uploadMapImage">
                                    Hochladen
                                </Button>
                            </div>
                        </fieldset>
                        <fieldset class="flex w-full flex-col gap-6 rounded-lg border p-4">
                            <legend class="-ml-1 px-1 text-sm font-medium">Ausgewählten Marker bearbeiten</legend>
                            <div class="h-[150px] w-full" v-if="map && map.imgUrl && map.imgWidth && map.imgHeight">
                                <Preview :map-img-url="map?.imgUrl" :map-img-width="map?.imgWidth"
                                    :map-img-height="map?.imgHeight" :marker="null" class="rounded-md" />
                            </div>
                            <div class="flex flex-col gap-3">
                                <Label for="name">Name</Label>
                                <UInput id="name" type="text" autocomplete="off" placeholder="Gebäude B" />
                                <Label for="description">Beschreibung</Label>
                                <Textarea id="description" type="text" placeholder="Aufzüge sind kapput!" />
                                <Label for="type">Stil</Label>
                                <div class="flex gap-3">
                                    <Select id="type" class="flex">
                                        <SelectTrigger class="w-full">
                                            <SelectValue placeholder="Select a type" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectGroup>
                                                <SelectLabel>Marker Typ</SelectLabel>
                                                <SelectItem v-for="icon in ['wheelchair', 'warning', 'info', 'default']"
                                                    :value="icon" :key="icon">
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
                                    <UInput id="color" type="color" autocomplete="off" class="max-w-[250px]" />
                                </div>
                                <Button variant="destructive" type="button">
                                    Löschen
                                </Button>
                                <Button variant="secondary" type="button">
                                    Ändern
                                </Button>
                            </div>
                        </fieldset>
                    </div>
                </aside>
            </ResizablePanel>
            <ResizableHandle with-handle />
            <ResizablePanel>
                <View v-if="map && map.imgHeight && map.imgWidth" @leaflet-ready="onMapReady" @create-marker="() => { }"
                    @marker-clicked="() => { }" @marker-location-update="() => { }" :map-img-url="map.imgUrl"
                    :map-img-width="map.imgWidth!" :map-img-height="map.imgHeight!" :markers="map.markers" />
                <div v-else class="flex h-full w-full items-center justify-center">
                    <p class="text-center text-3xl font-semibold">
                        Kein Kartenbild gefunden
                    </p>
                </div>
            </ResizablePanel>
        </ResizablePanelGroup>
    </Layout>
</template>
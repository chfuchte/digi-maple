<script setup lang="ts">
import { ref } from "vue";
import {type LatLng, Map} from "leaflet";
import { useHead } from "@unhead/vue";
import Layout from "@/components/layouts/default.vue";
import MapCreateView from "@/components/map/CreateView.vue";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

const devMapImagePath = "dev/Lageplan_Campus_Bockenheim.svg";
const imageHeightWidthRatio = 0.94285675588;
const height = 2000;
const width = imageHeightWidthRatio * height;

interface IMarker {
  id: string;
  name: string;
  description: string;
  lng: number;
  lat: number;
}

let leafletObject: Map | null = null;

let selectedMarker = ref<number | null>();

let markers = ref<Array<IMarker>>([]);
let title = ref("Neue Karte");
let description = ref("");

let markerNameModel = defineModel<string>("markerNameModel");
let markerDescriptionModel = defineModel<string>("markerDescriptionModel");
let descriptionModel = defineModel<string>("descriptionModel");
descriptionModel.value = description.value;
let titleModel = defineModel<string>("titleModel");
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
    name: "Marker",
    description: "Lorem Ipsum....",
    lng: leafletObject!.getCenter().lng,
    lat: leafletObject!.getCenter().lat
  });
}

function deleteMarker(): void {
  const marker = selectedMarker.value!;

  selectedMarker.value = null;

  markers.value = markers.value.filter((_, index) => index !== marker);

  console.log(markers.value);

  //markerNameModel.value = "";
  //markerDescriptionModel.value = "";
}

function editMarker(name: string, description: string): void {
  markers.value[selectedMarker.value!].description = description;
  markers.value[selectedMarker.value!].name = name;
}

function markerClicked(id: string): void {
  console.log("clicked: " + id);

  let marker = markers.value.findIndex((marker) => marker.id == id);

  selectedMarker.value = marker;
  markerNameModel.value =  markers.value[marker].name;
  markerDescriptionModel.value = markers.value[marker].description;
}

function markerLocationUpdated(id: string, location: LatLng): void {
  let marker = markers.value.findIndex((marker) => marker.id == id);

  markers.value[marker].lng = location.lng;
  markers.value[marker].lat = location.lat;
}
</script>

<template>
    <Layout>
      <div class="flex h-full">
        <aside class="bg-white border-black border-r p-4 w-1/3 overflow-y-auto">
          <form class="flex flex-col w-full items-start gap-6">
            <fieldset class="flex flex-col gap-6 rounded-lg border p-4 w-full">
              <legend class="-ml-1 px-1 text-sm font-medium">
                Settings
              </legend>
              <div class="flex flex-col gap-3">
                <Label for="name">Name</Label>
                <Input v-model:model-value="titleModel" id="name" type="text" placeholder="Campus Bockenheim" autocomplete="off" />
                <Label for="description">Description</Label>
                <Textarea v-model:model-value="descriptionModel"  id="description" type="text" placeholder="Eine Karte mit verschiedenen Markern." />
                <Button @click="title = titleModel!; description = descriptionModel!;" variant="secondary" type="button" :disabled="title == titleModel && description == descriptionModel">
                  Speichern
                </Button>
              </div>
            </fieldset>
            <fieldset class="flex flex-col gap-6 rounded-lg border p-4 w-full" :disabled="selectedMarker == null">
              <legend class="-ml-1 px-1 text-sm font-medium">
                Edit marker
              </legend>
              <div class="flex flex-col gap-3">
                <Label for="name">Name</Label>
                <Input v-model:model-value="markerNameModel" id="name" type="text" autocomplete="off" placeholder="Gebäude B" />
                <Label for="description">Description</Label>
                <Textarea v-model:model-value="markerDescriptionModel" id="description" type="text" placeholder="Aufzüge sind kapput!" />
                <Button variant="destructive" @click="deleteMarker()" type="button" :disabled="selectedMarker == null">
                  Löschen
                </Button>
                <Button variant="secondary" @click="editMarker(markerNameModel!, markerDescriptionModel!)" type="button" :disabled="selectedMarker != null && markers[selectedMarker].name == markerNameModel && markers[selectedMarker].description == markerDescriptionModel">
                  Ändern
                </Button>
              </div>
            </fieldset>
          </form>
        </aside>
        <MapCreateView
            @leaflet-ready="onMapReady"
            @create-marker="createMarker"
            @marker-clicked="markerClicked"
            @marker-location-update="markerLocationUpdated"
            :map-img-url="devMapImagePath"
            :map-img-width="width"
            :map-img-height="height"
            :markers="markers" />
      </div>
    </Layout>
</template>

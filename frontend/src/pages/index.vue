<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { MagnifyingGlassIcon } from "@radix-icons/vue";
import { apiSearchMaps } from "@/queries/maps";
import { Fragment, ref } from "vue";
import type { Map } from "@/typings/map";
import { toast } from "vue-sonner";

let searchTimeout: ReturnType<typeof setTimeout> | null = null;
const searchResults = ref<Array<Map>>([]);

const handleSearchInput = (e: { target: { value: string } }) => {
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }

    searchTimeout = setTimeout(async () => {
        const searchResult = await apiSearchMaps(e.target.value);

        if (searchResult === false) {
            toast.error("Fehler beim Abrufen der Daten", {
                description: "Bitte versuche es später erneut.",
            });
            searchResults.value = [];
            return;
        }

        searchResults.value = searchResult;
    }, 500);
};
</script>

<template>
    <Layout>
        <div class="my-4 w-full border-0 px-4 relative items-center">
            <Input @input="handleSearchInput" id="search" type="text" placeholder="Suche..." class="w-full pl-10" />
            <span class="absolute inset-y-0 start-0 flex items-center justify-center px-6">
                <MagnifyingGlassIcon class="size-6 text-muted-foreground" />
            </span>
        </div>
        <div class="w-full">
            <CardHeader v-if="searchResults.length === 0">
                <CardTitle class="text-2xl font-semibold">Keine Karten gefunden</CardTitle>
                <CardDescription>
                    Es konnte keine Karten gefunden werden, die deiner Anfrage entsprechen.
                </CardDescription>
            </CardHeader>
            <Fragment v-else>
                <CardHeader>
                    <CardTitle class="text-2xl font-semibold">Suchergebnisse</CardTitle>
                    <CardDescription>Hier sind die Suchergebnisse für deine Anfrage.</CardDescription>
                </CardHeader>
                <div class="flex gap-4 px-4 flex-wrap flex-row w-full">
                    <RouterLink class="max-w-80 w-3/4" v-for="map in searchResults" :to="`/maps/${map.id}`"
                        :key="map.id">
                        <Card class="w-full">
                            <CardHeader>
                                <CardTitle>{{ map.name }}</CardTitle>
                            </CardHeader>
                            <CardContent class="flex justify-center">
                                <img :src="map.imgUrl" alt="Map Image" class="h-auto w-full" />
                            </CardContent>
                        </Card>
                    </RouterLink>
                </div>
            </Fragment>
        </div>
    </Layout>
</template>

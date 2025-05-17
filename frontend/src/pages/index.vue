<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { MagnifyingGlassIcon } from "@radix-icons/vue";
import { apiSearchMaps } from "@/queries/maps";
import { onBeforeMount, ref } from "vue";
import type { Map } from "@/typings/map";
import { toast } from "vue-sonner";

let searchTimeout: ReturnType<typeof setTimeout> | null = null;
const emptySearch = ref<boolean>(true);
const searchResults = ref<Array<Map>>([]);

const handleSearchInput = (e: { target: { value: string } }) => {
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }

    searchTimeout = setTimeout(async () => {
        if (e.target.value === "") {
            emptySearch.value = true;
        } else {
            emptySearch.value = false;
        }

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

onBeforeMount(async () => {
    const searchResult = await apiSearchMaps("");
    emptySearch.value = true;

    if (searchResult === false) {
        toast.error("Fehler beim Abrufen der Daten", {
            description: "Bitte versuche es später erneut.",
        });
        searchResults.value = [];
        return;
    }

    searchResults.value = searchResult;
});
</script>

<template>
    <Layout>
        <div class="relative my-4 w-full items-center border-0 px-4">
            <Input @input="handleSearchInput" id="search" type="text" placeholder="Suche..." class="w-full pl-10" />
            <span class="absolute inset-y-0 start-0 flex items-center justify-center px-6">
                <MagnifyingGlassIcon class="size-6 text-muted-foreground" />
            </span>
        </div>
        <div class="w-full">
            <div v-if="searchResults.length > 0">
                <CardHeader v-if="emptySearch">
                    <CardTitle class="text-2xl font-semibold">
                        Karten durchsuchen - Zeige nur die ersten {{ searchResults.length || 10 }} Karten an
                    </CardTitle>
                    <CardDescription>
                        Bitte gib einen Suchbegriff ein, um weitere Karten zu finden.
                    </CardDescription>
                </CardHeader>
                <CardHeader v-else>
                    <CardTitle class="text-2xl font-semibold">Suchergebnisse</CardTitle>
                    <CardDescription>Hier sind die Suchergebnisse für deine Anfrage.</CardDescription>
                </CardHeader>
                <div class="flex w-full flex-row flex-wrap gap-4 px-4">
                    <RouterLink class="w-[90dvw] max-w-80" v-for="map in searchResults" :to="`/maps/${map.id}`"
                        :key="map.id">
                        <Card class="w-full">
                            <CardHeader>
                                <CardTitle>{{ map.name }}</CardTitle>
                            </CardHeader>
                            <CardContent class="flex h-[300px] items-center justify-center bg-background">
                                <div v-if="map.imgHeight && map.imgWidth"
                                    :style="`background-image: url(${map.imgUrl}); background-repeat: no-repeat; background-size: cover; background-position: center center;`"
                                    class="h-full w-full" />
                                <p v-else class="text-center text-2xl font-semibold">Bitte Kartenbild hochgeladen</p>
                            </CardContent>
                        </Card>
                    </RouterLink>
                </div>
            </div>
            <CardHeader v-else>
                <CardTitle class="text-2xl font-semibold">Keine Karten gefunden</CardTitle>
                <CardDescription>
                    Es konnte keine Karten gefunden werden, die deiner Anfrage entsprechen.
                </CardDescription>
            </CardHeader>
        </div>
    </Layout>
</template>

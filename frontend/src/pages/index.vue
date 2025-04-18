<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { MagnifyingGlassIcon } from "@radix-icons/vue";
import { apiSearchMaps } from "@/queries/maps";

let searchTimeout: ReturnType<typeof setTimeout> | null = null;

const search = (e: { target: { value: string } }) => {
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }

    searchTimeout = setTimeout(async () => {
        const searchResult = await apiSearchMaps(e.target.value);

        if (searchResult === false) {
            alert("Fehler beim Abrufen der Daten");
            return;
        }

        if (searchResult.length === 0) {
            alert("Keine Daten gefunden");
            return;
        }

        // TODO: Handle search results
    }, 500);
};
</script>

<template>
    <Layout>
        <Card class="w-full">
            <CardContent class="w-full px-0">
                <div class="relative w-full items-center">
                    <Input @input="search" id="search" type="text" placeholder="Suche..." class="w-full pl-10" />
                    <span class="absolute inset-y-0 start-0 flex items-center justify-center px-2">
                        <MagnifyingGlassIcon class="size-6 text-muted-foreground" />
                    </span>
                </div>
            </CardContent>
        </Card>
    </Layout>
</template>

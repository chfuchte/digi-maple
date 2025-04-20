<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import CreateDialog from "@/components/CreateDialog.vue";
import { onBeforeMount, ref } from "vue";
import type { Map } from "@/typings/map";
import { apiDeleteMap, apiGetUserMaps } from "@/queries/maps";
import { useRouter } from "vue-router";
import { CardFooter, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { AlertDialog, AlertDialogTrigger, AlertDialogTitle, AlertDialogContent, AlertDialogAction, AlertDialogHeader, AlertDialogFooter, AlertDialogDescription, AlertDialogCancel } from "@/components/ui/alert-dialog";

const router = useRouter();
const maps = ref<Map[] | null>(null);

onBeforeMount(async () => {
    const mapRes = await apiGetUserMaps();

    if (!mapRes) {
        await router.push("/");
        return;
    }

    maps.value = mapRes;
});

function handleDeleteMap(id: number): void {
    const deleteResult = apiDeleteMap(id);
    if (!deleteResult) {
        alert("Fehler beim Löschen der Karte.");
        return;
    }
    maps.value = maps.value?.filter((map) => map.id !== id) ?? null;
    alert("Karte erfolgreich gelöscht.");
}
</script>

<template>
    <Layout>
        <div class="w-full">
            <CardHeader class="flex flex-row items-center justify-between p-4">
                <CardTitle class="text-2xl font-semibold">Deine Karten</CardTitle>
                <CreateDialog />
            </CardHeader>
            <div class="flex gap-4 px-4 flex-wrap flex-row w-full">
                <Card class="max-w-80 w-3/4" v-for="map in maps" :to="`/map/${map.id}`" :key="map.id">
                    <CardHeader>
                        <CardTitle>{{ map.name }}</CardTitle>
                    </CardHeader>
                    <CardContent class="flex justify-center">
                        <img :src="map.imgUrl" alt="Map Image" class="h-auto w-full" />
                    </CardContent>
                    <CardFooter>
                        <RouterLink :to="`/map/${map.id}`">
                            <Button variant="outline" class="w-full">
                                Bearbeiten
                            </Button>
                        </RouterLink>
                        <AlertDialog>
                            <AlertDialogTrigger>
                                <Button variant="destructive" class="w-full">
                                    Löschen
                                </Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent>
                                <AlertDialogHeader>
                                    <AlertDialogTitle>Map löschen</AlertDialogTitle>
                                    <AlertDialogDescription>
                                        Bist du sicher, dass du diese Map löschen möchtest? Diese Aktion kann nicht
                                        rückgängig gemacht werden.
                                    </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter class="flex gap-2">
                                    <AlertDialogAction asChild>
                                        <Button @click="handleDeleteMap(map.id)" variant="destructive" class="flex-1">
                                            Löschen
                                        </Button>
                                    </AlertDialogAction>
                                    <AlertDialogCancel>
                                        <Button variant="outline" class="flex-1">
                                            Abbrechen
                                        </Button>
                                    </AlertDialogCancel>
                                </AlertDialogFooter>
                            </AlertDialogContent>
                        </AlertDialog>
                    </CardFooter>
                </Card>
            </div>
        </div>
    </Layout>
</template>

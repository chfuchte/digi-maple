<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import CreateDialog from "@/components/map/CreateDialog.vue";
import { onBeforeMount, ref } from "vue";
import type { Map } from "@/typings/map";
import { apiDeleteMap, apiGetUserMaps } from "@/queries/maps";
import { useRouter } from "vue-router";
import { CardFooter, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import {
    AlertDialog,
    AlertDialogTrigger,
    AlertDialogTitle,
    AlertDialogContent,
    AlertDialogAction,
    AlertDialogHeader,
    AlertDialogFooter,
    AlertDialogDescription,
    AlertDialogCancel,
} from "@/components/ui/alert-dialog";
import { toast } from "vue-sonner";

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
        toast.error("Fehler beim Löschen der Karte.", {
            description: "Bitte versuche es später erneut.",
        });
        return;
    }
    maps.value = maps.value?.filter((map) => map.id !== id) ?? null;
    toast.success("Karte erfolgreich gelöscht.");
}
</script>

<template>
    <Layout>
        <div class="w-full">
            <CardHeader class="flex flex-row items-center justify-between p-4">
                <CardTitle class="text-2xl font-semibold">Deine Karten</CardTitle>
                <CreateDialog />
            </CardHeader>
            <div class="flex w-full flex-row flex-wrap gap-4 px-4 max-sm:justify-center">
                <Card class="w-[90dvw] max-w-80" v-for="map in maps" :key="map.id">
                    <CardHeader>
                        <CardTitle>{{ map.name }}</CardTitle>
                    </CardHeader>
                    <CardContent class="flex h-[300px] items-center justify-center bg-background">
                        <div
                            v-if="map.imgHeight && map.imgWidth"
                            :style="`background-image: url(${map.imgUrl}); background-repeat: no-repeat; background-size: cover; background-position: center center;`"
                            class="h-full w-full" />
                        <p v-else class="text-center text-2xl font-semibold">Bitte Kartenbild hochgeladen</p>
                    </CardContent>
                    <CardFooter class="flex flex-wrap gap-2">
                        <div class="flex-1">
                            <RouterLink :to="`/maps/${map.id}/edit`" class="w-full">
                                <Button variant="outline" class="w-full"> Bearbeiten </Button>
                            </RouterLink>
                        </div>
                        <div class="flex-1">
                            <AlertDialog>
                                <AlertDialogTrigger asChild>
                                    <Button variant="destructive" class="w-full"> Löschen </Button>
                                </AlertDialogTrigger>
                                <AlertDialogContent>
                                    <AlertDialogHeader>
                                        <AlertDialogTitle>Karte löschen</AlertDialogTitle>
                                        <AlertDialogDescription>
                                            Bist du sicher, dass du diese Karte löschen möchtest? <br />
                                            Diese Aktion kann nicht rückgängig gemacht werden.
                                        </AlertDialogDescription>
                                    </AlertDialogHeader>
                                    <AlertDialogFooter class="flex gap-2">
                                        <AlertDialogAction asChild>
                                            <Button @click="handleDeleteMap(map.id)" class="flex-1"> Löschen </Button>
                                        </AlertDialogAction>
                                        <AlertDialogCancel asChild>
                                            <Button variant="outline" class="flex-1"> Abbrechen </Button>
                                        </AlertDialogCancel>
                                    </AlertDialogFooter>
                                </AlertDialogContent>
                            </AlertDialog>
                        </div>
                    </CardFooter>
                </Card>
            </div>
        </div>
    </Layout>
</template>

<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { useRouter } from "vue-router";
import { Button } from "@/components/ui/button";
import { LucidePlusCircle } from "lucide-vue-next";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import {
    AlertDialog,
    AlertDialogDescription,
    AlertDialogHeader,
    AlertDialogTrigger,
    AlertDialogTitle,
    AlertDialogContent,
    AlertDialogFooter,
    AlertDialogCancel,
    AlertDialogAction,
} from "@/components/ui/alert-dialog";
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { ref } from "vue";

const router = useRouter();

const file = ref<File | null>();
const titleModel = defineModel<string>("titleModel");
titleModel.value = "";

let uploading = ref<boolean>(false);

function upload(): void {
    if (file.value == null || titleModel.value == null) {
        return;
    }

    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": file.value!.type,
        },
        body: file.value!,
    }).then(() => {
        router.push("/create");
    });
}
</script>

<template>
    <Layout>
        <div class="flex flex-col gap-8 p-8">
            <div class="flex flex-row justify-between">
                <h1 class="text-3xl font-semibold">Dashboard</h1>
                <Dialog>
                    <DialogTrigger>
                        <Button>
                            <LucidePlusCircle />
                            Neue Karte
                        </Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle> Neue Karte erstellen </DialogTitle>
                        </DialogHeader>
                        <div class="flex w-full flex-col items-start gap-4">
                            <div class="flex w-full flex-col gap-1.5">
                                <Label for="title">Titel</Label>
                                <Input
                                    v-bind:model-value="titleModel"
                                    id="title"
                                    type="text"
                                    placeholder="Disney Land" />
                            </div>
                            <div class="flex w-full flex-col gap-1.5">
                                <Label for="picture">Kartenbild</Label>
                                <!-- TODO: event: any; find type -->
                                <Input
                                    id="picture"
                                    type="file"
                                    @change="(event: any) => (file = event.target.files[0])" />
                            </div>
                        </div>
                        <DialogFooter>
                            <DialogClose>
                                <Button variant="outline"> Zurück </Button>
                            </DialogClose>
                            <Button @click="upload()" :disabled="file == null || titleModel == ''"> Erstellen </Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>
            <div class="column-layout grid gap-4">
                <Card v-for="_ in 8">
                    <CardHeader>
                        <CardTitle>Test Map</CardTitle>
                    </CardHeader>
                    <CardContent class="flex justify-center">
                        <img src="/dev/preview.png" alt="An example preview map" width="250" />
                    </CardContent>
                    <CardFooter class="flex flex-row justify-between">
                        <Button>Öffnen</Button>
                        <AlertDialog>
                            <AlertDialogTrigger>
                                <Button variant="destructive"> Löschen </Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent>
                                <AlertDialogHeader>
                                    <AlertDialogTitle> Bist du dir sicher? </AlertDialogTitle>
                                    <AlertDialogDescription>
                                        Deine Map wird unwideruflich gelöscht!
                                    </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                    <AlertDialogCancel>Zurück</AlertDialogCancel>
                                    <AlertDialogAction>Löschen</AlertDialogAction>
                                </AlertDialogFooter>
                            </AlertDialogContent>
                        </AlertDialog>
                    </CardFooter>
                </Card>
            </div>
        </div>
    </Layout>
</template>

<style>
.column-layout {
    grid-template-columns: repeat(auto-fit, minmax(14rem, auto));
}
</style>

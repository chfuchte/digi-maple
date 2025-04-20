<script setup lang="ts">
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Input as UIInput } from "./ui/input";
import { ref } from "vue";
import { apiCreateMap, apiUploadMapImg } from "@/queries/maps";
import { LucidePlusCircle } from "lucide-vue-next";
import { Button } from "./ui/button";
import { Label } from "./ui/label";

const titleModel = defineModel<string>("titleModel");
const file = ref<File | null>();

async function handleUpload(): Promise<void> {
    if (!file.value || !titleModel.value) {
        alert("Bitte Titel und Datei angeben.");
        return;
    }

    const createResult = await apiCreateMap(titleModel.value);
    if (createResult === null) {
        alert("Fehler beim Erstellen der Karte.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file.value!);

    const uploadResult = await apiUploadMapImg(file.value, createResult);
    if (!uploadResult) {
        alert("Fehler beim Hochladen des Bildes.");
        return;
    }
}
</script>

<template>
    <Dialog>
        <DialogTrigger>
            <Button>
                <LucidePlusCircle />
                Neue Karte
            </Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Neue Karte erstellen</DialogTitle>
            </DialogHeader>
            <div class="flex w-full flex-col items-start gap-4">
                <div class="flex w-full flex-col gap-1.5">
                    <Label for="title">Titel</Label>
                    <UIInput v-model="titleModel" id="title" type="text" placeholder="Disney Land" />
                </div>
                <div class="flex w-full flex-col gap-1.5">
                    <Label for="picture">Datei</Label>
                    <input type="file" @input="(event: any) => (file = event.target.files[0])" />
                </div>
            </div>
            <DialogFooter>
                <DialogClose>
                    <Button variant="outline"> Abbrechen </Button>
                </DialogClose>
                <Button @click="handleUpload()" :disabled="!file || titleModel == ''">Erstellen</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
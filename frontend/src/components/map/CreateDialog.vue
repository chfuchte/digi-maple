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
import { Input as UIInput } from "../ui/input";
import { apiCreateMap } from "@/queries/maps";
import { LucidePlusCircle, LucideCircleAlert } from "lucide-vue-next";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const titleModel = defineModel<string>("titleModel");
const router = useRouter();

async function handleCreate(): Promise<void> {
    if (!titleModel.value) {
        alertMessage.value = "Bitte einen Titel angeben!";
        showAlert.value = true;
        return;
    }

    const createResult = await apiCreateMap(titleModel.value);
    if (createResult === null) {
        alertMessage.value = "Beim Erstellen der Karte ist ein Fehler aufgetaucht!";
        showAlert.value = true;
        return;
    }

    await router.push(`/maps/${createResult}/edit`);
}

const alertMessage = ref("");
const showAlert = ref(false);
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
                    <UIInput v-model="titleModel" id="title" type="text" placeholder="Disney Land" required />
                    <Alert variant="destructive" v-if="showAlert">
                        <LucideCircleAlert class="h-4 w-4" />
                        <AlertTitle>Fehler</AlertTitle>
                        <AlertDescription> {{ alertMessage }} </AlertDescription>
                    </Alert>
                </div>
            </div>
            <DialogFooter>
                <DialogClose>
                    <Button variant="outline"> Abbrechen </Button>
                </DialogClose>
                <Button @click="handleCreate()" :disabled="titleModel == ''">Erstellen</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

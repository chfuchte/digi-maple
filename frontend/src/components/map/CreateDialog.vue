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
import { LucidePlusCircle } from "lucide-vue-next";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { useRouter } from "vue-router";
import { toast } from "vue-sonner";

const titleModel = defineModel<string>("titleModel");
const router = useRouter();

async function handleCreate(): Promise<void> {
    if (!titleModel.value) {
        return;
    }

    const createResult = await apiCreateMap(titleModel.value);
    if (createResult === null) {
        toast.error("Fehler beim Erstellen der Karte.", {
            description: "Bitte versuchen Sie es später erneut.",
        });
        return;
    }

    await router.push(`/maps/${createResult}/edit`);
    toast.success("Karte erfolgreich erstellt.");
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
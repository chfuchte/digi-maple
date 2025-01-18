<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { Button } from '@/components/ui/button';
import { LucidePlusCircle } from 'lucide-vue-next';
import {Card, CardContent, CardFooter, CardHeader, CardTitle} from "@/components/ui/card";
import {
  AlertDialog,
  AlertDialogDescription,
  AlertDialogHeader,
  AlertDialogTrigger,
  AlertDialogTitle,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogCancel,
  AlertDialogAction
} from "@/components/ui/alert-dialog";
import {
  Dialog,
  DialogClose,
  DialogContent, DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {ref} from "vue";

let file = ref<File | null>();

function upload(): void {
  let formData = new FormData();
  formData.append('image', file.value);
}
</script>

<template>
  <Layout>
    <div class="p-8 flex flex-col gap-8">
      <div class="flex flex-row justify-between">
        <h1 class="text-3xl font-semibold">
          Dashboard
        </h1>
        <Dialog>
          <DialogTrigger>
            <Button>
              <LucidePlusCircle />
              Neue Karte
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>
                Neue Karte erstellen
              </DialogTitle>
              <DialogDescription>
                Bitte lade ein Bild deiner Karte hoch.
              </DialogDescription>
            </DialogHeader>
            <div class="grid w-full max-w-sm items-center gap-1.5">
              <Label for="picture">Kartenbild</Label>
              <Input
                  id="picture"
                  type="file"
                  @change="(event) => file = event.target.files[0]"
              />
            </div>
            <DialogFooter>
              <DialogClose>
                <Button variant="outline">
                  Zurück
                </Button>
              </DialogClose>
              <Button @click="upload()">
                Erstellen
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
      <div class="grid grid-cols-5 gap-4 h-auto">
        <Card v-for="_ in 8">
          <CardHeader>
            <CardTitle>Test Map</CardTitle>
          </CardHeader>
          <CardContent>
            <img src="/dev/preview.png" alt="An example preview map" width="250" />
          </CardContent>
          <CardFooter class="flex flex-row justify-between">
            <Button>Öffnen</Button>
            <AlertDialog>
              <AlertDialogTrigger>
                <Button variant="destructive">
                  Löschen
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>
                    Bist du dir sicher?
                  </AlertDialogTitle>
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
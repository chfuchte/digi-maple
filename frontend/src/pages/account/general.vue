<script setup lang="ts">
import SettingsLayout from "@/components/layouts/settings.vue";

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
</script>

<template>
    <SettingsLayout>
        <Card>
            <CardHeader>
                <CardTitle>Benutzername ändern</CardTitle>
            </CardHeader>
            <CardContent class="flex flex-col gap-2">
                <div>
                    <Label for="username">Neuer Benutzername</Label>
                    <Input id="username" type="text" placeholder="Pupsbaerchen" />
                </div>
                <div>
                    <Label for="password">Passwort</Label>
                    <Input id="password" type="password" placeholder="Pupsbaerchensonderzeichen1!" />
                </div>
            </CardContent>
            <CardFooter class="border-t px-6 py-4">
                <Button> Ändern </Button>
            </CardFooter>
        </Card>
        <Card>
            <CardHeader>
                <CardTitle>E-Mail ändern</CardTitle>
            </CardHeader>
            <CardContent class="flex flex-col gap-2">
                <div>
                    <Label for="mail">Neue E-Mail</Label>
                    <Input id="mail" type="email" placeholder="test@test.de" />
                </div>
                <div>
                    <Label for="password">Passwort</Label>
                    <Input id="password" type="password" placeholder="Pupsbaerchensonderzeichen1!" />
                </div>
            </CardContent>
            <CardFooter class="border-t px-6 py-4">
                <Button> Ändern </Button>
            </CardFooter>
        </Card>
        <Card>
            <CardHeader>
                <CardTitle>Account löschen</CardTitle>
            </CardHeader>
            <CardContent class="flex flex-col gap-2">
                <div>
                    <Label for="password">Passwort</Label>
                    <Input id="password" type="password" placeholder="Pupsbaerchensonderzeichen1!" />
                </div>
            </CardContent>
            <CardFooter class="border-t px-6 py-4">
                <Button variant="destructive"> Ändern </Button>
            </CardFooter>
        </Card>
    </SettingsLayout>
</template>

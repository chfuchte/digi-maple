<script setup lang="ts">
import SettingsLayout from "@/components/layouts/settings.vue";

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
</script>

<template>
    <SettingsLayout>
        <div class="flex w-full flex-col gap-4">
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
        </div>
    </SettingsLayout>
</template>

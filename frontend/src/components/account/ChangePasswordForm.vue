<script setup lang="ts">
import { z } from "zod";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { toast } from "vue-sonner";
import { useRouter } from "vue-router";
import { apiChangePassword } from "@/queries/account";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";

const router = useRouter();

// Schema for password change
const schema = z.object({
    oldPassword: z.string().min(1, "Altes Passwort ist erforderlich."),
    newPassword: z
        .string()
        .min(8, "Das Passwort muss mindestens 8 Zeichen lang sein.")
        .regex(
            /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).+$/,
            "Mindestens ein Großbuchstabe, ein Kleinbuchstabe, eine Zahl und ein Sonderzeichen.",
        ),
});
type FormValues = z.infer<typeof schema>;

const form = useForm({
    validationSchema: toTypedSchema(schema),
});

// Submit handler
const onSubmit = async (values: FormValues) => {
    const success = await apiChangePassword(values.oldPassword, values.newPassword);
    if (success) {
        toast.success("Passwort erfolgreich geändert.");
        await router.push("/");
    } else {
        form.resetForm();
        toast.error("Fehler beim Ändern des Passworts. Bitte versuchen Sie es erneut.");
    }
};
</script>

<template>
    <form @submit.prevent="(e) => form.handleSubmit(onSubmit)(e)">
        <Card class="w-[90svw] max-w-[450px]">
            <CardHeader>
                <CardTitle>Passwort ändern</CardTitle>
                <CardDescription> Ändere dein Passwort, um dein Konto zu schützen. </CardDescription>
            </CardHeader>
            <CardContent>
                <FormField v-slot="{ componentField }" name="oldPassword">
                    <FormItem>
                        <FormLabel>Altes Passwort</FormLabel>
                        <FormControl>
                            <Input type="password" placeholder="Altes Passwort" v-bind="componentField" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                </FormField>

                <FormField v-slot="{ componentField }" name="newPassword">
                    <FormItem>
                        <FormLabel>Neues Passwort</FormLabel>
                        <FormControl>
                            <Input type="password" placeholder="Neues Passwort" v-bind="componentField" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                </FormField>
            </CardContent>
            <CardFooter>
                <Button type="submit" class="w-full">Passwort ändern</Button>
            </CardFooter>
        </Card>
    </form>
</template>

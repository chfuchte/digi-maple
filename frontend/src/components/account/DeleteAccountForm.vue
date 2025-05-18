<script setup lang="ts">
import { z } from "zod";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { useRouter } from "vue-router";
import { toast } from "vue-sonner";
import { apiDeleteAccount } from "@/queries/account";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    FormField,
    FormItem,
    FormLabel,
    FormControl,
    FormMessage,
} from "@/components/ui/form";

const router = useRouter();

const schema = z.object({
    password: z.string().min(1, "Passwort ist erforderlich."),
});
type FormValues = z.infer<typeof schema>;

const form = useForm({
    validationSchema: toTypedSchema(schema),
});

const onSubmit = async (values: FormValues) => {
    const success = await apiDeleteAccount(values.password);
    if (success) {
        toast.success("Konto erfolgreich gelöscht.");
        await router.push("/");
    } else {
        form.resetForm();
        toast.error("Fehler beim Löschen des Kontos. Bitte versuchen Sie es erneut.");
    }
};
</script>

<template>
    <form @submit.prevent="(e) => form.handleSubmit(onSubmit)(e)">
        <Card class="w-[90svw] max-w-[450px]">
            <CardHeader>
                <CardTitle>Account löschen</CardTitle>
                <CardDescription>
                    Diese Aktion kann nicht rückgängig gemacht werden. Mit der Löschung deines Kontos werden
                    alle deine Daten inklusive deiner Karten gelöscht. Bitte gib dein Passwort ein, um
                    fortzufahren.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <FormField v-slot="{ componentField }" name="password">
                    <FormItem>
                        <FormLabel>Passwort</FormLabel>
                        <FormControl>
                            <Input type="password" placeholder="Passwort" v-bind="componentField" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                </FormField>
            </CardContent>
            <CardFooter>
                <Button type="submit" class="w-full" variant="destructive">Account löschen</Button>
            </CardFooter>
        </Card>
    </form>
</template>

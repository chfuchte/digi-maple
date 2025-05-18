<script setup lang="ts">
import { useForm } from "vee-validate";
import { z } from "zod";
import { toTypedSchema } from "@vee-validate/zod";
import { apiChangeEmail } from "@/queries/account";
import { toast } from "vue-sonner";
import { useRouter } from "vue-router";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";

const router = useRouter();

const schema = z.object({
    email: z.string().email(),
    password: z.string(),
});
const form = useForm({
    validationSchema: toTypedSchema(schema),
});
type FormValues = z.infer<typeof schema>;

const onSubmit = async (values: FormValues) => {
    const success = await apiChangeEmail(values.email, values.password);
    if (success) {
        toast.success("E-Mail erfolgreich geändert.");
        await router.push("/");
    } else {
        form.resetForm();
        toast.error("Fehler beim Ändern der E-Mail.");
    }
};
</script>

<template>
    <form @submit.prevent="(e) => form.handleSubmit(onSubmit)(e)">
        <Card class="w-[90svw] max-w-[450px]">
            <CardHeader>
                <CardTitle>E-Mail ändern</CardTitle>
                <CardDescription>
                    Aktualisiere deine E-Mail-Adresse, um Benachrichtigungen zu erhalten.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <FormField v-slot="{ componentField }" name="email">
                    <FormItem>
                        <FormLabel>E-Mail</FormLabel>
                        <FormControl>
                            <Input type="email" placeholder="deine@email.com" v-bind="componentField" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                </FormField>
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
                <Button type="submit" class="w-full">E-Mail ändern</Button>
            </CardFooter>
        </Card>
    </form>
</template>

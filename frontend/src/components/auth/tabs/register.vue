<script setup lang="ts">
import { apiRegister } from "@/queries/register";
import { toTypedSchema } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import { useRouter } from "vue-router";
import { z } from "zod";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { FormField, FormControl, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Button } from "@/components/ui/button";

const formSchema = z.object({
    fullName: z.string(),
    email: z.string().email("Bitte geben Sie eine gültige E-Mail-Adresse ein."),
    password: z
        .string()
        .min(8, "Das Passwort muss mindestens 8 Zeichen lang sein.")
        .regex(
            /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]+$/,
            "Das Passwort muss mindestens einen Großbuchstaben, einen Kleinbuchstaben, eine Zahl und ein Sonderzeichen enthalten.",
        ),
});

const typedFormSchema = toTypedSchema(formSchema);

type RegisterForm = z.infer<typeof formSchema>;

const registerform = useForm({
    validationSchema: typedFormSchema,
});

const onRegisterSubmit = (values: RegisterForm) => {
    apiRegister(values.fullName, values.email, values.password).then((registerSuccess) => {
        if (registerSuccess) {
            useRouter().push("/auth");
        } else {
            // TODO: Show error message
            alert("Fehler bei der Registrierung.");
        }
    });
};
</script>

<template>
    <form
        @submit="
            (e) => {
                e.preventDefault();
                registerform.handleSubmit(onRegisterSubmit)(e);
            }
        "
        :validation-schema="registerform">
        <Card>
            <CardHeader>
                <CardTitle>Registrierung</CardTitle>
                <CardDescription> Change your password here. After saving, you'll be logged out. </CardDescription>
            </CardHeader>
            <CardContent class="space-y-2">
                <FormField v-slot="{ componentField }" name="fullName">
                    <FormItem>
                        <FormLabel>Vollständiger Name</FormLabel>
                        <FormControl>
                            <Input type="text" placeholder="Vorname Nachname" v-bind="componentField" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                </FormField>

                <FormField v-slot="{ componentField }" name="email">
                    <FormItem>
                        <FormLabel>E-Mail</FormLabel>
                        <FormControl>
                            <Input type="email" placeholder="vorname.nachname@email.com" v-bind="componentField" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                </FormField>

                <FormField v-slot="{ componentField }" name="password">
                    <FormItem>
                        <FormLabel>Passwort</FormLabel>
                        <FormControl>
                            <Input type="password" placeholder="Pupsbaerchensonderzeichen1!" v-bind="componentField" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                </FormField>
            </CardContent>
            <CardFooter>
                <Button type="submit" class="w-full">Registrierung abschließen</Button>
            </CardFooter>
        </Card>
    </form>
</template>

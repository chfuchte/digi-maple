<script setup lang="ts">
import { toTypedSchema } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import { useRouter } from "vue-router";
import { z } from "zod";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { FormField, FormItem, FormControl, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { apiLogin } from "@/queries/auth";

const formSchema = z.object({
    email: z.string().email("Bitte geben Sie eine gültige E-Mail-Adresse ein."),
    password: z.string(),
});

const router = useRouter();

if (!router) {
    console.log("Router not found");
}

const typedFormSchema = toTypedSchema(formSchema);

type LoginForm = z.infer<typeof formSchema>;

const loginForm = useForm({
    validationSchema: typedFormSchema,
});

const onloginSubmit = async (values: LoginForm) => {
    const loginSuccess = await apiLogin(values.email, values.password);
    if (loginSuccess) {
        await router.push("/");
    } else {
        loginForm.resetForm();
        // TODO: Show error message
        alert("Fehler bei dem Login.");
    }
};
</script>

<template>
    <form
        @submit="
            (e) => {
                e.preventDefault();
                loginForm.handleSubmit(onloginSubmit)(e);
            }
        "
        :validation-schema="loginForm">
        <Card>
            <CardHeader>
                <CardTitle>Anmeldung</CardTitle>
                <CardDescription> Melden Sie sich hier an. </CardDescription>
            </CardHeader>
            <CardContent class="space-y-2">
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
                <Button type="submit" class="w-full">Anmelden</Button>
            </CardFooter>
        </Card>
    </form>
</template>

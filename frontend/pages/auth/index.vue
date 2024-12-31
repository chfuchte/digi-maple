<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm, Form as VForm } from 'vee-validate'
import { z } from 'zod'

const tab = ref("login")

definePageMeta({
    layout: "auth"
})

useHead({
    title: computed(() => tab.value === "login" ? "Anmelden" : "Registrieren")
})

onMounted(() => {
    if (window.location.hash === "#register") {
        tab.value = "register"
    }
})

const loginFormSchema = toTypedSchema(z.object({
    email: z.string().email("Bitte geben Sie eine gültige E-Mail-Adresse ein."),
    password: z.string()
}))
const loginform = useForm({
    validationSchema: loginFormSchema,
})
const onLoginSubmit = loginform.handleSubmit(async (values) => {
    apiLogin(values.email, values.password).then(res => {
        if (res) {
            navigateTo("/create");
        } else {
            // TODO: Show error message
            alert("Fehler bei der Anmeldung.")
        }
    })
})

const registerFormSchema = toTypedSchema(z.object({
    fullName: z.string(),
    email: z.string().email("Bitte geben Sie eine gültige E-Mail-Adresse ein."),
    password: z.string().min(8, "Das Passwort muss mindestens 8 Zeichen lang sein.").regex(/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]+$/, "Das Passwort muss mindestens einen Großbuchstaben, einen Kleinbuchstaben, eine Zahl und ein Sonderzeichen enthalten.")
}))
const registerform = useForm({
    validationSchema: registerFormSchema,
})
const onRegisterSubmit = registerform.handleSubmit((values) => {
    apiRegister(values.fullName, values.email, values.password).then(registerSuccess => {
        if (registerSuccess) {
            tab.value = "login"
        } else {
            // TODO: Show error message
            alert("Fehler bei der Registrierung.")
        }
    })
})

</script>

<template>
    <Tabs v-model="tab" class="w-[90svw] max-w-[450px]">
        <TabsList class="grid w-full grid-cols-2">
            <TabsTrigger value="login">
                Anmelden
            </TabsTrigger>
            <TabsTrigger value="register">
                Registrieren
            </TabsTrigger>
        </TabsList>
        <TabsContent value="login">
            <VForm :form="loginform" as="div">
                <form @submit="onLoginSubmit">
                    <Card>
                        <CardHeader>
                            <CardTitle>Anmeldung</CardTitle>
                            <CardDescription>
                                Falls Sie noch kein Konto haben, können Sie sich
                                <span class="underline" @click="tab = 'register'">hier</span> registrieren.
                            </CardDescription>
                        </CardHeader>
                        <CardContent class="space-y-2">
                            <FormField v-slot="{ componentField }" name="email">
                                <FormItem>
                                    <FormLabel>E-Mail</FormLabel>
                                    <FormControl>
                                        <Input type="email" placeholder="vorname.nachname@email.com"
                                            v-bind="componentField" />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            </FormField>

                            <FormField v-slot="{ componentField }" name="password">
                                <FormItem>
                                    <FormLabel>Passwort</FormLabel>
                                    <FormControl>
                                        <Input type="password" placeholder="Pupsbaerchensonderzeichen1!"
                                            v-bind="componentField" />
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
            </VForm>
        </TabsContent>

        <TabsContent value="register">
            <VForm :form="registerform" as="div">
                <form @submit="onRegisterSubmit">
                    <Card>
                        <CardHeader>
                            <CardTitle>Registrierung</CardTitle>
                            <CardDescription>
                                Change your password here. After saving, you'll be logged out.
                            </CardDescription>
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
                                        <Input type="email" placeholder="vorname.nachname@email.com"
                                            v-bind="componentField" />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            </FormField>

                            <FormField v-slot="{ componentField }" name="password">
                                <FormItem>
                                    <FormLabel>Passwort</FormLabel>
                                    <FormControl>
                                        <Input type="password" placeholder="Pupsbaerchensonderzeichen1!"
                                            v-bind="componentField" />
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
            </VForm>
        </TabsContent>
    </Tabs>
</template>

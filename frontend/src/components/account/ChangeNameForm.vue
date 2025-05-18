<script setup lang="ts">
import { z } from "zod";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { apiChangeName } from "@/queries/account";
import { toast } from "vue-sonner";
import { useRouter } from "vue-router";
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
import { useCurrentUserStore } from "@/stores/user";

const router = useRouter();
const {fetch} = useCurrentUserStore();

const schema = z.object({
    fullName: z.string().min(1, "Name darf nicht leer sein."),
});
type FormValues = z.infer<typeof schema>;

const form = useForm({
    validationSchema: toTypedSchema(schema),
});

const onSubmit = async (values: FormValues) => {
    const success = await apiChangeName(values.fullName);
    if (success) {
        toast.success("Name erfolgreich geändert.");
        await fetch();
        await router.push("/");
    } else {
        form.resetForm();
        toast.error("Fehler beim Ändern des Namens. Bitte versuchen Sie es erneut.");
    }
};
</script>

<template>
    <form @submit.prevent="(e) => form.handleSubmit(onSubmit)(e)">
        <Card class="w-[90svw] max-w-[450px]">
            <CardHeader>
                <CardTitle>Name ändern</CardTitle>
                <CardDescription>
                    Aktualisiere deinen Namen, welcher auf deinem Profil angezeigt wird.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <FormField v-slot="{ componentField }" name="fullName">
                    <FormItem>
                        <FormLabel>Vollständiger Name</FormLabel>
                        <FormControl>
                            <Input type="text" placeholder="Vorname Nachname" v-bind="componentField" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                </FormField>
            </CardContent>
            <CardFooter>
                <Button type="submit" class="w-full">Name ändern</Button>
            </CardFooter>
        </Card>
    </form>
</template>

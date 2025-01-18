<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useHead } from '@unhead/vue'
import AuthLayout from '@/components/layouts/auth.vue';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import AuthTabsLogin from '@/components/auth/tabs/login.vue';
import AuthTabsRegister from '@/components/auth/tabs/register.vue';

const tab = ref("login");

useHead({
    title: computed(() => (tab.value === "login" ? "Anmelden" : "Registrieren")),
});

onMounted(() => {
    if (window.location.hash === "#register") {
        tab.value = "register";
    }
});
</script>

<template>
    <AuthLayout>
        <Tabs v-model="tab" class="w-[90svw] max-w-[450px]">
            <TabsList class="grid w-full grid-cols-2">
                <TabsTrigger value="login"> Anmelden </TabsTrigger>
                <TabsTrigger value="register"> Registrieren </TabsTrigger>
            </TabsList>
            <TabsContent value="login">
                <AuthTabsLogin />
            </TabsContent>

            <TabsContent value="register">
                <AuthTabsRegister />
            </TabsContent>
        </Tabs>
    </AuthLayout>
</template>

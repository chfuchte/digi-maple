<script setup lang="ts">
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
            <AuthTabsLogin />
        </TabsContent>

        <TabsContent value="register">
            <AuthTabsRegister />
        </TabsContent>
    </Tabs>
</template>

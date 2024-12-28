<script setup lang="ts">

const { getUser } = useCurrentUserStore()
const user = computed(() => getUser())

const colorMode = useColorMode()

console.log(colorMode.value)

const toggleColorMode = () => {
    colorMode.preference = colorMode.preference === 'light' ? 'dark' : 'light';
}

</script>

<template>
    <header class="flex h-12 items-center justify-between px-4 shadow-sm">
        <NuxtLink to="/" class="my-2 flex items-center gap-3">
            <div class="flex items-center gap-1">
                <LucideMap :size="30" />
                <h1 class="text-3xl">Maple</h1>
            </div>
        </NuxtLink>

        <NuxtLink to="/auth/logout" v-if="user">
            <Button variant="secondary">Abmelden</Button>
        </NuxtLink>
        <NuxtLink to="/auth" v-else>
            <Button variant="secondary">Anmelden</Button>
        </NuxtLink>

        <DropdownMenu>
            <DropdownMenuTrigger as-child>
                <Button variant="ghost">
                    <LucideEllipsisVertical />
                    <span class="sr-only">Einstellungen</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuItem @click="toggleColorMode">
                    <LucideSunMoon />
                    <span>Toggle Dark Mode</span>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    </header>
</template>

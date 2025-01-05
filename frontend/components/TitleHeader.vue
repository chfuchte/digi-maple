<script setup lang="ts">
const { getUser } = useCurrentUserStore()
const user = getUser()

const colorMode = useColorMode()

const toggleColorMode = () => {
    colorMode.preference = colorMode.preference === 'light' ? 'dark' : 'light';
}

const logout = async () => {
    await useCurrentUserStore().logout()
    await navigateTo("/");
}

</script>

<template>
    <header class="flex h-12 items-center justify-between px-4 border-b border-secondary">
        <NuxtLink to="/" class="my-2 flex items-center gap-3">
            <div class="flex items-center gap-1">
                <LucideMap :size="30" />
                <h1 class="text-3xl">Maple</h1>
            </div>
        </NuxtLink>

        <div class="flex items-center gap-2">
            <a v-if="user">
                <Button @click="logout" variant="link">Abmelden</Button>
            </a>
            <NuxtLink to="/auth" v-else>
                <Button variant="link">Anmelden</Button>
            </NuxtLink>

            <DropdownMenu>
                <DropdownMenuTrigger as-child>
                    <Button variant="ghost">
                        <LucideEllipsisVertical />
                        <span class="sr-only">Einstellungen</span>
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    <DropdownMenuItem @click="toggleColorMode" class="flex items-center justify-end gap-2">
                        <LucideSunMoon />
                        <span>Toggle Dark Mode</span>
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    </header>
</template>

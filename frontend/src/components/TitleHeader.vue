<script setup lang="ts">
import { useCurrentUserStore } from '@/stores/user';
import { useColorMode } from '@vueuse/core';
import { useRouter, RouterLink } from "vue-router";
import { LucideMap, LucideEllipsisVertical, LucideSunMoon } from 'lucide-vue-next';
import { Button } from './ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from './ui/dropdown-menu';

const { getUser } = useCurrentUserStore();
const user = getUser();

const router = useRouter();

const colorMode = useColorMode({
    initialValue: "auto",
    attribute: "class",
    selector: "html",
});

const toggleColorMode = () => {
    colorMode.value = colorMode.value === "light" ? "dark" : "light";
};

const logout = async () => {
    await useCurrentUserStore().logout();;
    await router.push("/auth");
};
</script>

<template>
    <header class="flex h-12 items-center justify-between border-b border-secondary px-4">
        <RouterLink to="/" class="my-2 flex items-center gap-3">
            <div class="flex items-center gap-1">
                <LucideMap :size="30" />
                <h1 class="text-3xl">Maple</h1>
            </div>
        </RouterLink>

        <div class="flex items-center gap-2">
            <a v-if="user">
                <Button @click="logout" variant="link">Abmelden</Button>
            </a>
            <RouterLink to="/auth" v-else>
                <Button variant="link">Anmelden</Button>
            </RouterLink>

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

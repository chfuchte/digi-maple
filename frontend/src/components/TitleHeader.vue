<script setup lang="ts">
import { useCurrentUserStore } from "@/stores/user";
import { useColorMode } from "@vueuse/core";
import { useRouter, RouterLink } from "vue-router";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    DropdownMenuSeparator,
    DropdownMenuLabel,
} from "./ui/dropdown-menu";
import {
    LucideCircleUser,
    LucideLogOut,
    LucideLogIn,
    LucideMoon,
    LucideSun,
    LucideMap,
    LucideHome,
} from "lucide-vue-next";
import { onBeforeMount, ref } from "vue";

const { getUser, logout } = useCurrentUserStore();
const router = useRouter();

const user = ref<Awaited<ReturnType<typeof getUser>>>(null)

const colorMode = useColorMode({
    initialValue: "auto",
    attribute: "class",
    selector: "html",
});

onBeforeMount(async () => {
    user.value = await getUser();
});

const toggleColorMode = () => {
    colorMode.value = colorMode.value === "light" ? "dark" : "light";
};

const handleLogout = async () => {
    await logout();
    await router.push("/auth");
};
</script>

<template>
    <header class="flex h-12 items-center justify-between border-b px-4">
        <nav class="flex items-center flex-row truncate gap-4">
            <RouterLink to="/" class="my-2 mr-2 flex items-center gap-3">
                <div class="flex items-center flex-row gap-1">
                    <LucideMap :size="30" />
                    <h1 class="text-3xl">Maple</h1>
                </div>
            </RouterLink>
            <RouterLink v-if="user" to="/dashboard"
                class="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
                Dashboard
            </RouterLink>
        </nav>

        <div class="flex items-center gap-2">
            <Button @click="toggleColorMode" variant="ghost" size="icon">
                <template v-if="colorMode === 'dark'">
                    <LucideSun />
                </template>
                <template v-else>
                    <LucideMoon />
                </template>
            </Button>

            <DropdownMenu v-if="user">
                <DropdownMenuTrigger>
                    <Button variant="secondary" size="icon" class="rounded-full">
                        <LucideCircleUser class="h-5 w-5" />
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                    <template v-if="user">
                        <DropdownMenuLabel class="flex font-normal">
                            <div class="flex flex-col space-y-1">
                                <p class="text-sm font-medium leading-none">
                                    {{ user.full_name }}
                                </p>
                            </div>
                        </DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <RouterLink to="/dashboard">
                            <DropdownMenuItem class="cursor-pointer">
                                <LucideHome />
                                <span>Dashboard</span>
                            </DropdownMenuItem>
                        </RouterLink>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem @click="handleLogout" class="cursor-pointer">
                            <LucideLogOut />
                            <span>Abmelden</span>
                        </DropdownMenuItem>
                    </template>
                </DropdownMenuContent>
            </DropdownMenu>
            <RouterLink to="/auth" v-else>
                <Button variant="ghost">
                    <LucideLogIn />
                    <span>Anmelden</span>
                </Button>
            </RouterLink>
        </div>
    </header>
</template>

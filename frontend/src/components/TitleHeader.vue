<script setup lang="ts">
import { useCurrentUserStore } from '@/stores/user';
import { useColorMode } from '@vueuse/core';
import { useRouter, RouterLink } from "vue-router";
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuSeparator, DropdownMenuLabel } from './ui/dropdown-menu';
import { LucideCircleUser, LucideLogOut, LucideLogIn, LucideUser, LucideMoon, LucideSun, LucideMap } from 'lucide-vue-next';

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
    await useCurrentUserStore().logout();
    await router.push("/auth");
};
</script>

<template>
    <header class="flex h-12 items-center justify-between border-b px-4">
        <nav class="flex gap-4 items-center">
          <RouterLink to="/" class="my-2 flex items-center gap-3 mr-2">
            <div class="flex items-center gap-1">
              <LucideMap :size="30" />
              <h1 class="text-3xl">Maple</h1>
            </div>
          </RouterLink>
          <RouterLink to="/dashboard" class="text-muted-foreground transition-colors hover:text-foreground text-sm font-medium">
            Dashboard
          </RouterLink>
        </nav>

        <div class="flex items-center gap-2">
          <Button @click="toggleColorMode" variant="ghost">
            <template v-if="colorMode === 'dark'">
              <LucideSun />
            </template>
            <template v-else>
              <LucideMoon />
            </template>
          </Button>

            <DropdownMenu>
              <DropdownMenuTrigger>
                <Button variant="secondary" size="icon" class="rounded-full">
                  <LucideCircleUser class="h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <template v-if="user">
                  <DropdownMenuLabel class="font-normal flex">
                    <div class="flex flex-col space-y-1">
                      <p class="text-sm font-medium leading-none">
                        {{user.full_name}}
                      </p>
                      <p class="text-xs leading-none text-muted-foreground">
                        3 Maps
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <LucideUser />
                    <span>Account</span>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem @click="logout">
                    <LucideLogOut />
                    <span>Abmelden</span>
                  </DropdownMenuItem>
                </template>
                <RouterLink to="/auth" v-else>
                  <DropdownMenuItem>
                    <LucideLogIn />
                    <span>Anmelden</span>
                  </DropdownMenuItem>
                </RouterLink>
              </DropdownMenuContent>
            </DropdownMenu>
        </div>
    </header>
</template>

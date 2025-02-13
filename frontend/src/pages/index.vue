<script setup lang="ts">
import Layout from "@/components/layouts/welcome.vue";
import { CardContent } from "@/components/ui/card";
import { Input as UInput } from "@/components/ui/input";
import { MagnifyingGlassIcon } from "@radix-icons/vue";

let searchTimeout: NodeJS.Timeout | null = null;

const search = (e: { target: { value: string } }) => {
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }

    searchTimeout = setTimeout(() => {
        // fetch data
        // TODO
        console.log(e.target.value);
    }, 500);
};
</script>

<template>
    <Layout>
        <Card class="w-full">
            <CardContent class="w-full px-0">
                <div class="relative w-full items-center">
                    <UInput @input="search" id="search" type="text" placeholder="Suche..." class="w-full pl-10" />
                    <span class="absolute inset-y-0 start-0 flex items-center justify-center px-2">
                        <MagnifyingGlassIcon class="size-6 text-muted-foreground" />
                    </span>
                </div>
            </CardContent>
        </Card>
    </Layout>
</template>

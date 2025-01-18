<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { Button } from "@/components/ui/button";
import { RouterLink } from "vue-router";
</script>

<template>
    <!-- TODO: transform to a welcome page of the "product" -->
    <Layout>
        <div class="flex h-full flex-grow flex-col items-center justify-center gap-4">
            <RouterLink to="/maps/dev">
                <Button size="lg" class="w-80" variant="default"> Development Map </Button>
            </RouterLink>
            <RouterLink to="/create">
                <Button size="lg" class="w-80" variant="default"> Create Map </Button>
            </RouterLink>
        </div>
    </Layout>
</template>

<script setup lang="ts"></script>

<template>
    <!-- TODO: transform to a welcome page of the "product" -->
    <div class="flex flex-grow flex-col h-full items-center justify-center gap-4">
        <NuxtLink to="/maps/dev">
            <Button size="lg" class="w-80" variant="default"> Development Map </Button>
        </NuxtLink>
        <NuxtLink to="/create">
            <Button size="lg" class="w-80" variant="default"> Create Map </Button>
        </NuxtLink>
    </div>
</template>

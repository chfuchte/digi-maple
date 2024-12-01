<script setup lang="ts">
</script>

<template>
    <TitleHeader />
    <div class="flex-grow bg-gray-200 flex flex-col gap-3 items-center justify-center text-black">
        <h1 class="text-3xl">Test oder so</h1>
        <NuxtLink to="/maps/">
            <Button variant="secondary">
                Example Map
            </Button>
        </NuxtLink>
        <NuxtLink to="/create">
            <Button variant="secondary">
                Create
            </Button>
        </NuxtLink>
    </div>
</template>

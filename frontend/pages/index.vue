<script setup lang="ts"></script>

<template>
    <TitleHeader />
    <div class="flex flex-grow flex-col items-center justify-center gap-3 bg-gray-200 text-black">
        <h1 class="text-3xl">Test oder so</h1>
        <NuxtLink to="/maps/">
            <Button variant="secondary"> Example Map </Button>
        </NuxtLink>
        <NuxtLink to="/create">
            <Button variant="secondary"> Create </Button>
        </NuxtLink>
    </div>
</template>

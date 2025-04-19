<script setup lang="ts">
import TitleHeader from "../TitleHeader.vue";
</script>

<template>
    <TitleHeader />
    <div class="mx-16 flex gap-16">
        <main class="flex w-full flex-col gap-4 pt-8">
            <slot />
        </main>
    </div>
</template>

<style>
/* TODO: extract to css file */
:root {
    --header-height: 48px;
}

header {
    height: var(--header-height);
}

main {
    height: calc(100dvh - var(--header-height));
}
</style>

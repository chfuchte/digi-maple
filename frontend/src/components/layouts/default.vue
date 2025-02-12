<script setup lang="ts">
import TitleHeader from "../TitleHeader.vue";
</script>

<template>
    <TitleHeader />
    <main>
        <slot />
    </main>
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

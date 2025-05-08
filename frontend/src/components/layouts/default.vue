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
main {
    height: calc(100dvh - 48px);
}
</style>

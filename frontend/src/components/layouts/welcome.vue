<script setup lang="ts"></script>

<template>
    <main>
        <slot />
    </main>
</template>

<style>
main {
    min-height: 100dvh;
    @apply box-border px-2 py-4;
}
</style>

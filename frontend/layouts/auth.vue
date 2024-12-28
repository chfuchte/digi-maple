<script setup lang="ts">

onMounted(async () => {
    const { getUser } = useCurrentUserStore();
    const user = getUser();
    if (user) {
        return navigateTo('/');
    }
})
</script>

<template>
    <main class="grid place-items-start justify-center max-sm:py-6 py-20">
        <slot />
    </main>
</template>

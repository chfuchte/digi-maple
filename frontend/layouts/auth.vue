<script setup lang="ts">
onBeforeMount(async () => {
    const { getUser } = useCurrentUserStore();
    const user = getUser();
    if (user) {
        return await navigateTo('/');
    }
})
</script>

<template>
    <main class="grid place-items-center w-dvw h-dvh">
        <slot />
    </main>
</template>

<script setup lang="ts">
let title = ref<string | undefined>(undefined);

onMounted(() => {
    title.value = document.title;
});
</script>

<template>
    <header class="flex items-center justify-between border-b-2 h-12 border-b-black bg-white px-4 text-black">
        <div class="my-2 flex items-center gap-3">
            <div class="flex items-center gap-1">
                <LucideMap :size="30" />
                <h1 class="text-3xl">Maple</h1>
            </div>
            <div v-if="title" class="h-5 w-0.5 bg-black"></div>
            <h3 v-if="title">
                {{ title }}
            </h3>
        </div>
        <slot />
    </header>
</template>

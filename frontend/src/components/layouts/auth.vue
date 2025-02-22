<script setup lang="ts">
import { useCurrentUserStore } from "@/stores/user";
import { onMounted } from "vue";
import { useRouter } from "vue-router";

onMounted(async () => {
    const { getUser } = useCurrentUserStore();
    const user = getUser();
    if (user) {
        useRouter().push("/");
    }
});
</script>

<template>
    <main class="grid place-items-start justify-center py-20 max-sm:py-6">
        <slot />
    </main>
</template>

<script setup lang="ts">
import { ref } from "vue";

let isExpanded = ref(false);

const { title = "" } = defineProps<{
    title?: string;
}>();
</script>

<template>
    <div class="flex items-start">
        <button class="border-black border-b border-l border-t p-1.5 rounded-l-md text-black"
                @click="isExpanded = !isExpanded"
                :class="{'bg-gray-100': isExpanded, 'bg-white': !isExpanded}">
            <LucideChevronLeft v-if="isExpanded" />
            <div class="flex mr-1.5" v-else>
                <LucideChevronRight />
                <h2 v-if="title != ''">{{ title }}</h2>
            </div>
        </button>
        <div class="w-96" :class="{'-mr-96': !isExpanded}">
            <slot />
        </div>
    </div>
</template>
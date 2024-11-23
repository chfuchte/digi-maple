<script setup lang="ts">
  const props = defineProps<{
    map: any,
  }>();
</script>

<template>
  <div class="absolute z-400 top-0 left-0">
    <Button v-on:click="props.map">
      <LucideChevronUp />
    </Button>
    <Button>
      <LucideChevronDown />
    </Button>
  </div>
</template>
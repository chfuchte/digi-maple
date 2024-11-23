<script setup lang="ts">
  import type {GlobalThis} from "type-fest";

  const props = defineProps<{
    map: globalThis.Ref<any, any>,
  }>();
</script>

<template>
  <div class="absolute z-400 top-0 left-0">
    <Button @click="console.log(props.map.value);">
      <LucideChevronUp />
    </Button>
    <Button>
      <LucideChevronDown />
    </Button>
  </div>
</template>
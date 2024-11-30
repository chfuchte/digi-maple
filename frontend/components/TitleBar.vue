<script setup lang="ts">
    import { Map } from 'lucide-vue-next';
</script>

<template>
  <header class="bg-white border-b-2 border-b-black text-black">
      <div class="flex items-center gap-3 my-2 mx-4">
          <div class="flex items-center gap-1">
              <Map :size="30" />
              <h1 class="text-3xl">Maple</h1>
          </div>
          <div class="w-0.5 h-5 bg-black"></div>
          <h3><slot /></h3>
      </div>
  </header>
</template>

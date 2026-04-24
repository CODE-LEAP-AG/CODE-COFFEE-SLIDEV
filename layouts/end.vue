<script setup lang="ts">
defineProps<{
  pageNumber?: number | string
  brand?: string
}>()
const currentYear = new Date().getFullYear()
</script>

<template>
  <div class="cc-layout cc-end">
    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>
    <div class="cc-end__inner">
      <h1 class="cc-end__title">
        Thank you all<span class="cc-accent">_</span>
      </h1>
      <p class="cc-end__subtitle">
        <slot>If you have questions, feel free to ask</slot>
      </p>
    </div>
    <footer class="cc-copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

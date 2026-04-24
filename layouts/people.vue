<script setup lang="ts">
interface Person {
  name: string
  team?: string
  role?: string
  avatar?: string
}

defineProps<{
  heading?: string
  people?: Person[]
  pageNumber?: number | string
  brand?: string
}>()
const currentYear = new Date().getFullYear()
</script>

<template>
  <div class="cc-layout cc-people">
    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>
    <header class="cc-content__header">
      <h2 v-if="heading" class="cc-content__title">
        {{ heading }}<span class="cc-accent">_</span>
      </h2>
    </header>
    <div class="cc-people__grid" :class="`cols-${people?.length || 2}`">
      <div v-for="p in people" :key="p.name" class="cc-people__card">
        <div class="cc-avatar">
          <img v-if="p.avatar" :src="p.avatar" :alt="p.name" />
          <span v-else class="cc-avatar__placeholder">{{ p.name.charAt(0) }}</span>
        </div>
        <div class="cc-people__name">{{ p.name }}</div>
        <div v-if="p.team" class="cc-people__team">{{ p.team }}</div>
        <div v-if="p.role" class="cc-people__role">{{ p.role }}</div>
      </div>
    </div>
    <footer class="cc-copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

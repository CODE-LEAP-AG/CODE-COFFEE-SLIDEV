<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  heading?: string
  subtitle?: string
  image?: string
  pageNumber?: number | string
  brand?: string
}>()

const currentYear = new Date().getFullYear()

const headingParts = computed(() => {
  const raw = props.heading?.trim()
  if (!raw) return null
  const idx = raw.lastIndexOf(' ')
  if (idx === -1) return { lead: '', tail: raw }
  return { lead: raw.slice(0, idx + 1), tail: raw.slice(idx + 1) }
})
</script>

<template>
  <div class="cc-layout cc-event">
    <img class="cc-event__pitch" src="/pitch.svg" alt="" aria-hidden="true" />
    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>

    <div class="cc-event__left">
      <header class="cc-event__header">
        <h2 v-if="headingParts" class="cc-event__title">
          <span v-if="headingParts.lead">{{ headingParts.lead }}</span><span class="cc-title-tail">{{ headingParts.tail }}<span class="cc-accent">_</span></span>
        </h2>
        <p v-if="subtitle" class="cc-event__subtitle">{{ subtitle }}</p>
      </header>
      <div class="cc-event__body">
        <slot />
      </div>
    </div>

    <div class="cc-event__right">
      <img
        v-if="image"
        :src="image"
        :alt="heading"
        class="cc-event__image"
      />
      <div v-else class="cc-event__placeholder" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
          <circle cx="8.5" cy="8.5" r="1.5" />
          <polyline points="21 15 16 10 5 21" />
        </svg>
        <span>No image</span>
      </div>
    </div>

    <footer class="cc-copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  heading?: string
  pageNumber?: number | string
  sectionIcon?: string
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
  <div class="cc-layout cc-section">
    <img class="cc-section__pitch" src="/pitch.svg" alt="" aria-hidden="true" />
    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>
    <img
      v-if="props.sectionIcon"
      class="cc-section__icon"
      :src="props.sectionIcon"
      alt=""
      aria-hidden="true"
    />
    <div class="cc-section__title">
      <template v-if="headingParts">
        <span v-if="headingParts.lead">{{ headingParts.lead }}</span><span class="cc-title-tail">{{ headingParts.tail }}<span class="cc-accent">_</span></span>
      </template>
      <slot v-else />
    </div>
    <footer class="cc-copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

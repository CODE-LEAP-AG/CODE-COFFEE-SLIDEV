<script setup lang="ts">
import { computed, useSlots } from 'vue'

const props = defineProps<{
  heading?: string
  subtitle?: string
  images?: string[]
  pageNumber?: number | string
  brand?: string
}>()

const currentYear = new Date().getFullYear()
const slots = useSlots()

const headingParts = computed(() => {
  const raw = props.heading?.trim()
  if (!raw) return null
  const idx = raw.lastIndexOf(' ')
  if (idx === -1) return { lead: '', tail: raw }
  return { lead: raw.slice(0, idx + 1), tail: raw.slice(idx + 1) }
})

const gallery = computed(() => {
  const list = (props.images ?? []).filter(Boolean)
  return list.slice(0, 3)
})
</script>

<template>
  <div class="cc-layout cc-office-update">
    <img class="cc-office-update__pitch" src="/pitch.svg" alt="" aria-hidden="true" />
    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>

    <header class="cc-office-update__header">
      <h2 v-if="headingParts" class="cc-office-update__title">
        <span v-if="headingParts.lead">{{ headingParts.lead }}</span><span class="cc-title-tail">{{ headingParts.tail }}<span class="cc-accent">_</span></span>
      </h2>
      <p v-if="subtitle" class="cc-office-update__subtitle">{{ subtitle }}</p>
    </header>

    <div v-if="slots.default" class="cc-office-update__body">
      <slot />
    </div>

    <div
      v-if="gallery.length"
      class="cc-office-update__gallery"
      :class="`cols-${gallery.length}`"
    >
      <figure
        v-for="(src, idx) in gallery"
        :key="`${src}-${idx}`"
        class="cc-office-update__frame"
      >
        <img
          :src="src"
          :alt="heading ? `${heading} — ${idx + 1}` : `${idx + 1}`"
        />
      </figure>
    </div>

    <footer class="cc-copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  headline?: string
  name?: string
  avatar?: string
  role?: string
  meta?: string
  highlight?: string
  logo?: string
  emoji?: string
  brand?: string
  pageNumber?: number | string
}>()

const certLogos = import.meta.glob('../assets/cert-logos/*.png', {
  eager: true,
  import: 'default',
}) as Record<string, string>

const logoSrc = computed(() => {
  if (!props.logo) return ''
  const match = Object.entries(certLogos).find(([key]) => {
    const file = key.split('/').pop()?.replace(/\.png$/i, '').toLowerCase()
    return file === props.logo!.toLowerCase()
  })
  return match?.[1] ?? ''
})

const currentYear = new Date().getFullYear()
</script>

<template>
  <div class="cc-layout cc-certification">
    <aside class="cc-certification__panel" aria-hidden="true"></aside>
    <img class="cc-certification__pitch" src="/pitch.svg" alt="" aria-hidden="true" />

    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>

    <div class="cc-certification__left">
      <h2 v-if="headline" class="cc-certification__headline">
        <span class="cc-certification__headline-text">{{ headline }}{{ emoji ? ` ${emoji}` : '' }}</span>
      </h2>

      <div class="cc-certification__details">
        <div v-if="name" class="cc-certification__name">
          <span>{{ name }}</span>
          <span class="cc-accent">_</span>
        </div>
        <p v-if="meta" class="cc-certification__meta">{{ meta }}</p>
        <div v-if="$slots.default" class="cc-certification__body">
          <slot />
        </div>
        <p v-if="highlight" class="cc-certification__highlight">{{ highlight }}</p>
        <div v-if="logoSrc" class="cc-certification__logo-wrap">
          <img
            class="cc-certification__logo"
            :src="logoSrc"
            alt="Logos by Brandfetch"
          />
        </div>
      </div>
    </div>

    <div class="cc-certification__right">
      <div class="cc-certification__photo">
        <img v-if="avatar" :src="avatar" :alt="name" />
        <span v-else class="cc-certification__photo-placeholder">
          {{ (name || '?').charAt(0) }}
        </span>
      </div>
      <div v-if="role" class="cc-certification__role">{{ role }}</div>
    </div>

    <footer class="cc-copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

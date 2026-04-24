<script setup lang="ts">
defineProps<{
  headline?: string
  name?: string
  role?: string
  meta?: string
  highlight?: string
  avatar?: string
  emoji?: string
  brand?: string
  pageNumber?: number | string
}>()
const currentYear = new Date().getFullYear()
</script>

<template>
  <div class="cc-layout cc-birthday">
    <div class="cc-birthday__backdrop" aria-hidden="true"></div>
    <div class="cc-birthday__veil" aria-hidden="true"></div>
    <aside class="cc-birthday__panel" aria-hidden="true"></aside>

    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>

    <div class="cc-birthday__left">
      <p v-if="headline" class="cc-birthday__headline">
        <span class="cc-birthday__headline-text">{{ headline }}</span><span class="cc-accent">_</span>
      </p>

      <div class="cc-birthday__details">
        <div v-if="name" class="cc-birthday__name">
          <span class="cc-birthday__name-text">{{ name }}</span>
          <span v-if="emoji" class="cc-birthday__emoji">{{ emoji }}</span>
        </div>
        <p v-if="meta" class="cc-birthday__meta">{{ meta }}</p>
        <div v-if="$slots.default" class="cc-birthday__body">
          <slot />
        </div>
        <p v-if="highlight" class="cc-birthday__highlight">{{ highlight }}</p>
      </div>
    </div>

    <div class="cc-birthday__right">
      <div class="cc-birthday__photo">
        <img v-if="avatar" :src="avatar" :alt="name" />
        <span v-else class="cc-birthday__photo-placeholder">
          {{ (name || '?').charAt(0) }}
        </span>
      </div>
      <div v-if="role" class="cc-birthday__role">{{ role }}</div>
    </div>

    <footer class="cc-copyright cc-birthday__copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

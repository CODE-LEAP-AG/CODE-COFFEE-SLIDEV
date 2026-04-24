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
  <div class="cc-layout cc-person cc-anniversary">
    <aside class="cc-person__panel" aria-hidden="true"></aside>

    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>

    <div class="cc-person__left">
      <span v-if="emoji" class="cc-anniversary__ornament">{{ emoji }}</span>

      <h2 v-if="headline" class="cc-person__headline">
        <span class="cc-person__headline-text">{{ headline }}</span>
      </h2>

      <div class="cc-person__details">
        <div v-if="name" class="cc-person__name">
          {{ name }}<span class="cc-accent">_</span>
        </div>
        <p v-if="meta" class="cc-person__meta">{{ meta }}</p>
        <div v-if="$slots.default" class="cc-person__body">
          <slot />
        </div>
        <p v-if="highlight" class="cc-person__highlight">{{ highlight }}</p>
      </div>
    </div>

    <div class="cc-person__right">
      <div class="cc-person__photo">
        <img v-if="avatar" :src="avatar" :alt="name" />
        <span v-else class="cc-person__photo-placeholder">
          {{ (name || '?').charAt(0) }}
        </span>
      </div>
      <div v-if="role" class="cc-person__role">{{ role }}</div>
    </div>

    <footer class="cc-copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

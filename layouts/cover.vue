<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  date?: string
  bgImage?: string
  bgBlur?: number
  brand?: string
}>()

const coverStyle = computed(() => {
  if (!props.bgImage) return {}
  return {
    '--cc-cover-bg-image': `url("${props.bgImage}")`,
    '--cc-cover-bg-blur': `${props.bgBlur ?? 14}px`,
  }
})
const currentYear = new Date().getFullYear()
</script>

<template>
  <div
    class="cc-layout cc-cover"
    :class="{
      'cc-cover--with-bg': !!props.bgImage,
      'cc-layout--brand-dark': !!props.bgImage,
    }"
    :style="coverStyle"
  >
    <div v-if="props.bgImage" class="cc-cover__bg" aria-hidden="true" />
    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>
    <div class="cc-cover__inner">
      <h1 class="cc-cover__title">
        Code Coffee<span class="cc-accent">_</span>
      </h1>
      <p v-if="date" class="cc-cover__date">{{ date }}</p>
      <slot />
    </div>
    <footer class="cc-copyright">© {{ currentYear }} CODE LEAP AG. All rights reserved.</footer>
  </div>
</template>

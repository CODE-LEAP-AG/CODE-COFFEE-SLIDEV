<script setup lang="ts">
import { computed } from 'vue'

interface TeamMember {
  name: string
  role?: string
  avatar?: string
  client?: boolean
}

const props = defineProps<{
  heading?: string
  subtitle?: string
  image?: string
  team?: TeamMember[]
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

const teamLayout = computed(() => {
  const count = props.team?.length ?? 0
  // cols + size variant — balance columns vs. per-card real estate so small
  // teams get big, poster-style cards and large teams stay legible.
  if (count <= 1) return { cols: 1, size: 'xl' }
  if (count <= 2) return { cols: 2, size: 'xl' }
  if (count <= 3) return { cols: 3, size: 'lg' }
  if (count <= 4) return { cols: 2, size: 'lg' } // 2x2 grid
  if (count <= 6) return { cols: 3, size: 'md' }
  if (count <= 8) return { cols: 4, size: 'md' }
  if (count <= 12) return { cols: 4, size: 'sm' }
  return { cols: 4, size: 'xs' }
})

function initial(name: string) {
  const parts = name.trim().split(/\s+/)
  return (parts[0]?.[0] ?? '?').toUpperCase()
}
</script>

<template>
  <div class="cc-layout cc-project" :class="`team-${teamLayout.size}`">
    <img class="cc-event__pitch" src="/pitch.svg" alt="" aria-hidden="true" />
    <div v-if="brand !== ''" class="cc-brand">
      {{ brand || 'CODE_LEAP' }}
    </div>

    <div class="cc-project__left">
      <img
        v-if="image"
        :src="image"
        :alt="heading"
        class="cc-project__logo"
      />
      <header class="cc-project__header">
        <h2 v-if="headingParts" class="cc-project__title">
          <span v-if="headingParts.lead">{{ headingParts.lead }}</span><span class="cc-title-tail">{{ headingParts.tail }}<span class="cc-accent">_</span></span>
        </h2>
        <p v-if="subtitle" class="cc-project__subtitle">{{ subtitle }}</p>
      </header>
      <div class="cc-project__body">
        <slot />
      </div>
    </div>

    <aside v-if="team && team.length" class="cc-project__right">
      <h3 class="cc-project__team-label">Team<span class="cc-accent">_</span></h3>
      <div
        class="cc-project__team-grid"
        :class="`size-${teamLayout.size}`"
        :style="{ '--team-cols': teamLayout.cols }"
      >
        <div
          v-for="p in team"
          :key="p.name"
          class="cc-project__member"
          :class="{ 'is-client': p.client }"
        >
          <div class="cc-project__avatar">
            <img v-if="p.avatar" :src="p.avatar" :alt="p.name" />
            <span v-else class="cc-project__avatar-placeholder">{{ initial(p.name) }}</span>
          </div>
          <div class="cc-project__member-text">
            <div class="cc-project__member-name">{{ p.name }}</div>
            <div v-if="p.role" class="cc-project__member-role">{{ p.role }}</div>
          </div>
        </div>
      </div>
    </aside>

    <footer class="cc-copyright">
      <span>© {{ currentYear }} CODE LEAP AG. All rights reserved.</span>
      <span v-if="pageNumber" class="cc-page-number">{{ pageNumber }}</span>
    </footer>
  </div>
</template>

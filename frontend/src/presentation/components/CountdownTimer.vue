<script setup lang="ts">
import { useCountdown } from '../composables/useCountdown'

const props = defineProps<{ target: Date }>()
const countdown = useCountdown(() => props.target)

const UNITS = [
  { key: 'days', label: 'Days' },
  { key: 'hours', label: 'Hours' },
  { key: 'minutes', label: 'Minutes' },
  { key: 'seconds', label: 'Seconds' },
] as const
</script>

<template>
  <p v-if="countdown.done" class="today">Today is the day</p>
  <div v-else class="countdown" role="timer" aria-label="Time until the wedding">
    <div v-for="unit in UNITS" :key="unit.key" class="unit">
      <span class="value">{{ countdown[unit.key] }}</span>
      <span class="label">{{ unit.label }}</span>
    </div>
  </div>
</template>

<style scoped>
.countdown {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: .6rem;
  margin: 1.5rem 0 2rem;
}

.unit {
  padding: .8rem .25rem;
  border-radius: 18px;
  background: var(--sage-100);
}

.unit:nth-child(2) { background: var(--blush-100); }
.unit:nth-child(3) { background: var(--lavender-100); }
.unit:nth-child(4) { background: var(--peach-100); }

.value {
  display: block;
  font: 600 clamp(1.6rem, 6vw, 2.1rem)/1 var(--font-serif);
  font-variant-numeric: tabular-nums;
}

.label {
  color: var(--ink-soft);
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .14em;
  text-transform: uppercase;
}

.today {
  margin: 1.5rem 0 2rem;
  color: var(--sage-700);
  font-family: var(--font-serif);
  font-size: 1.6rem;
}
</style>

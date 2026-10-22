<!-- Pastel sky, drifting clouds, rolling hills, a flower meadow and falling petals. -->
<script setup lang="ts">
import { useReducedMotion } from '../../composables/useReducedMotion'

const reducedMotion = useReducedMotion()

const COLORS = ['#f6cdd3', '#fde0cb', '#e6dcf5', '#fbe7a8', '#d7ecd9']
const count = window.innerWidth < 600 ? 10 : 18

const petals = Array.from({ length: count }, (_, i) => ({
  id: i,
  style: {
    left: `${Math.random() * 100}%`,
    '--size': `${8 + Math.random() * 10}px`,
    '--color': COLORS[i % COLORS.length],
    '--dur': `${12 + Math.random() * 12}s`,
    '--delay': `${-Math.random() * 24}s`,
    '--sway': `${(Math.random() * 2 - 1) * 120}px`,
  },
}))

const flowers = [
  { x: 80, y: 70, s: 1.1, fill: '#f6cbd1' },
  { x: 210, y: 86, s: 1, fill: '#e6dcf5' },
  { x: 340, y: 64, s: 1.15, fill: '#fde0cb' },
  { x: 520, y: 90, s: 1, fill: '#f6cbd1' },
  { x: 690, y: 72, s: 1.1, fill: '#e6dcf5' },
  { x: 860, y: 84, s: 1, fill: '#fde0cb' },
  { x: 1010, y: 66, s: 1.15, fill: '#f6cbd1' },
  { x: 1180, y: 88, s: 1, fill: '#e6dcf5' },
  { x: 1320, y: 74, s: 1.1, fill: '#fde0cb' },
]
const stems = flowers.map((f) => `M${f.x} ${f.y + 4}V120`).join('')
</script>

<template>
  <div class="scenery" aria-hidden="true">
    <div class="sun" />
    <div class="cloud cloud--1" />
    <div class="cloud cloud--2" />
    <div class="cloud cloud--3" />

    <svg class="hills" viewBox="0 0 1440 320" preserveAspectRatio="none">
      <path fill="#e3e5f4" d="M0 150 C220 70 460 70 720 130 C980 190 1210 90 1440 80 L1440 320 L0 320 Z" />
      <path fill="#d3ebd6" d="M0 210 C300 140 520 190 760 215 C1000 240 1240 170 1440 190 L1440 320 L0 320 Z" />
      <path fill="#bfdfc6" d="M0 265 C260 225 560 255 820 265 C1080 275 1260 245 1440 255 L1440 320 L0 320 Z" />
    </svg>

    <svg class="meadow" viewBox="0 0 1440 120" preserveAspectRatio="xMidYMax slice">
      <path fill="none" stroke="#94c29f" stroke-width="2.5" stroke-linecap="round" :d="stems" />
      <use
        v-for="(f, i) in flowers"
        :key="`leaf-${f.x}`"
        href="#leaf"
        :transform="`translate(${f.x} ${f.y + 30}) rotate(${i % 2 ? -140 : -40}) scale(.7)`"
        :fill="i % 2 ? '#93c2a1' : '#a9d1b3'"
      />
      <use
        v-for="f in flowers"
        :key="`flower-${f.x}`"
        href="#blossom"
        :transform="`translate(${f.x} ${f.y}) scale(${f.s})`"
        :fill="f.fill"
      />
    </svg>

    <div v-if="!reducedMotion" class="petals">
      <span v-for="p in petals" :key="p.id" class="petal" :style="p.style" />
    </div>
  </div>
</template>

<style scoped>
.scenery {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background: linear-gradient(180deg, #e6f0fb 0%, #f4ebf5 42%, #fdeee6 72%, #fff5e8 100%);
}

.sun {
  position: absolute;
  top: 5vh;
  right: 8vw;
  width: 240px;
  height: 240px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 236, 204, .95) 0%, rgba(255, 226, 200, .55) 42%, rgba(255, 226, 200, 0) 70%);
}

.cloud {
  position: absolute;
  left: 0;
  width: 160px;
  height: 48px;
  border-radius: 48px;
  background: rgba(255, 255, 255, .85);
  animation: drift linear infinite;
}

.cloud::before,
.cloud::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  background: inherit;
}

.cloud::before { width: 70px; height: 70px; top: -34px; left: 26px; }
.cloud::after { width: 54px; height: 54px; top: -24px; left: 82px; }

.cloud--1 { top: 12vh; animation-duration: 95s; animation-delay: -25s; }
.cloud--2 { top: 26vh; scale: .7; opacity: .8; animation-duration: 130s; animation-delay: -80s; }
.cloud--3 { top: 44vh; scale: .55; opacity: .7; animation-duration: 160s; animation-delay: -40s; }

@keyframes drift {
  from { translate: -260px 0; }
  to { translate: 110vw 0; }
}

.hills {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 34vh;
  min-height: 180px;
}

.meadow {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 12vh;
  min-height: 70px;
}

.petals { position: absolute; inset: 0; }

.petal {
  position: absolute;
  top: -5vh;
  width: var(--size);
  height: calc(var(--size) * .8);
  border-radius: 100% 0 100% 0;
  background: var(--color);
  opacity: .85;
  animation: fall var(--dur) linear var(--delay) infinite;
}

@keyframes fall {
  0% { transform: translate3d(0, -10vh, 0) rotate(0deg); }
  50% { transform: translate3d(var(--sway), 50vh, 0) rotate(200deg); }
  100% { transform: translate3d(calc(var(--sway) * -.5), 110vh, 0) rotate(420deg); }
}

@media (prefers-reduced-motion: reduce) {
  .cloud { animation: none; }
}
</style>

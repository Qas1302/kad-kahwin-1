<!--
  Decorative bird that flies between perches. It is positioned inside its offset parent
  (the stage), so it scrolls with the card. Call flyTo(perchElement) to move it.
-->
<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

import { prefersReducedMotion } from '../composables/useReducedMotion'

type BirdState = 'flying' | 'landing' | 'perched'
type Point = { x: number; y: number }

// Where the feet sit inside the bird graphic, as fractions of its box.
const FOOT_X = 0.475
const FOOT_Y = 0.91

const root = ref<HTMLElement | null>(null)
const tilt = ref<HTMLElement | null>(null)
const state = ref<BirdState | null>(null)
const facing = ref<'left' | 'right'>('right')
const singing = ref(false)

let pos: Point = { x: 0, y: 0 }
let perch: HTMLElement | null = null
let frame = 0
let settleTimer = 0
let songTimer = 0
let finishFlight: (() => void) | null = null
let resizeObserver: ResizeObserver | null = null

const clamp = (v: number, min: number, max: number) => Math.min(max, Math.max(min, v))
const easeInOut = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)

function bezier(p0: Point, p1: Point, p2: Point, p3: Point, t: number): Point {
  const u = 1 - t
  const a = u * u * u
  const b = 3 * u * u * t
  const c = 3 * u * t * t
  const d = t * t * t
  return {
    x: a * p0.x + b * p1.x + c * p2.x + d * p3.x,
    y: a * p0.y + b * p1.y + c * p2.y + d * p3.y,
  }
}

function place(point: Point) {
  const el = root.value
  if (!el) return
  pos = point
  const x = point.x - el.offsetWidth * FOOT_X
  const y = point.y - el.offsetHeight * FOOT_Y
  el.style.transform = `translate3d(${x}px, ${y}px, 0)`
}

/** Perch position relative to the stage, so it stays right while the page scrolls. */
function pointOf(target: HTMLElement): Point {
  const stage = (root.value?.offsetParent as HTMLElement | null) ?? document.body
  const s = stage.getBoundingClientRect()
  const r = target.getBoundingClientRect()
  return { x: r.left + r.width / 2 - s.left, y: r.top + r.height / 2 - s.top }
}

function land(target: HTMLElement) {
  place(pointOf(target))
  if (tilt.value) tilt.value.style.transform = ''
  facing.value = target.dataset.face === 'left' ? 'left' : 'right'
  state.value = 'landing'
  window.clearTimeout(settleTimer)
  settleTimer = window.setTimeout(() => {
    if (state.value === 'landing') state.value = 'perched'
  }, 400)
}

function flyTo(target: HTMLElement | null): Promise<void> {
  if (!target || !root.value) return Promise.resolve()

  // A new flight interrupts the current one and starts from wherever the bird is.
  cancelAnimationFrame(frame)
  finishFlight?.()
  perch = target

  if (prefersReducedMotion()) {
    land(target)
    return Promise.resolve()
  }

  const start = { ...pos }
  const goal = pointOf(target)
  const dx = goal.x - start.x
  const distance = Math.hypot(dx, goal.y - start.y)
  const duration = clamp(800 + distance * 1.2, 1300, 2400)
  const lift = clamp(distance * 0.35, 80, 200)
  const peak = Math.min(start.y, goal.y) - lift
  const c1 = { x: start.x + dx * 0.15, y: peak }
  const c2 = { x: start.x + dx * 0.85, y: peak + lift * 0.25 }

  if (Math.abs(dx) > 4) facing.value = dx < 0 ? 'left' : 'right'
  state.value = 'flying'

  return new Promise((resolve) => {
    finishFlight = () => {
      finishFlight = null
      resolve()
    }

    const t0 = performance.now()
    let prev = start

    const step = (now: number) => {
      const p = Math.min(1, (now - t0) / duration)
      // Track the perch live, since the section may still be sliding into place.
      const point = bezier(start, c1, c2, pointOf(target), easeInOut(p))
      const bob = Math.sin(p * Math.PI * 7) * 4 * Math.sin(p * Math.PI)
      place({ x: point.x, y: point.y + bob })

      // Pitch the body with the direction of travel.
      const pitch = Math.atan2(point.y - prev.y, Math.abs(point.x - prev.x) + 0.5) * (180 / Math.PI) * 0.6
      const dir = facing.value === 'left' ? -1 : 1
      if (tilt.value) tilt.value.style.transform = `rotate(${clamp(pitch, -22, 22) * dir}deg)`
      prev = point

      if (p < 1) {
        frame = requestAnimationFrame(step)
      } else {
        land(target)
        finishFlight?.()
      }
    }

    frame = requestAnimationFrame(step)
  })
}

/** Fly in from off-screen at the top left. */
function enter(target: HTMLElement | null): Promise<void> {
  const stage = root.value?.offsetParent as HTMLElement | null
  const left = stage?.getBoundingClientRect().left ?? 0
  place({ x: -left - 90, y: -140 })
  facing.value = 'right'
  return flyTo(target)
}

/** Keep the bird on its perch when the layout changes. */
function reperch() {
  if (state.value !== 'flying' && perch) place(pointOf(perch))
}

onMounted(() => {
  const stage = root.value?.parentElement
  if (stage) {
    resizeObserver = new ResizeObserver(reperch)
    resizeObserver.observe(stage)
  }
  window.addEventListener('resize', reperch)

  // Sing now and then while perched.
  songTimer = window.setInterval(() => {
    if (prefersReducedMotion() || document.hidden || state.value !== 'perched' || Math.random() < 0.4) return
    singing.value = true
    window.setTimeout(() => (singing.value = false), 1600)
  }, 6500)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(frame)
  window.clearTimeout(settleTimer)
  window.clearInterval(songTimer)
  resizeObserver?.disconnect()
  window.removeEventListener('resize', reperch)
})

defineExpose({ flyTo, enter, reperch })
</script>

<template>
  <div
    ref="root"
    class="bird"
    :class="[state && `is-${state}`, { 'is-singing': singing }]"
    :data-face="facing"
    aria-hidden="true"
  >
    <div ref="tilt" class="bird__tilt">
      <div class="bird__flip" :style="{ transform: `scaleX(${facing === 'left' ? -1 : 1})` }">
        <svg class="bird__svg" viewBox="0 0 120 100">
          <g class="bird__wing bird__wing--far"><path d="M72 50 C66 28 56 12 40 4 C46 22 52 38 58 52 Z" /></g>
          <path class="bird__tail" d="M34 54 L6 42 L12 57 L4 68 L36 63 Z" />
          <g class="bird__legs">
            <path d="M52 74 L50 89 M50 89 L44 92 M50 89 L53 92 M62 74 L63 89 M63 89 L58 92 M63 89 L67 92" />
          </g>
          <ellipse class="bird__torso" cx="56" cy="56" rx="30" ry="23" />
          <ellipse class="bird__belly" cx="63" cy="64" rx="20" ry="13" />
          <g class="bird__head">
            <circle class="bird__torso" cx="80" cy="38" r="17" />
            <path class="bird__crest" d="M75 23 C76 15 84 13 84 21" />
            <circle class="bird__cheek" cx="88" cy="46" r="4" />
            <g class="bird__eye">
              <circle cx="86" cy="35" r="3.2" fill="#3d4a44" />
              <circle cx="87.2" cy="33.8" r="1.1" fill="#fff" />
            </g>
            <path class="bird__beak" d="M95 35 L108 40 L95 45 Z" />
          </g>
          <path class="bird__wing-folded" d="M36 50 C48 38 66 40 74 52 C66 66 48 68 32 60 Z" />
          <g class="bird__wing bird__wing--near"><path d="M70 52 C62 30 48 12 30 6 C38 24 46 40 54 54 Z" /></g>
        </svg>
      </div>
    </div>
    <span class="bird__note">♪</span>
  </div>
</template>

<style scoped>
.bird {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 5;
  width: clamp(54px, 13vw, 76px);
  aspect-ratio: 6 / 5;
  pointer-events: none;
  transform: translate3d(-200vw, -50vh, 0);
  will-change: transform;
}

/* Rotations and flips pivot around the feet so the bird stays on its perch */
.bird__tilt,
.bird__flip {
  width: 100%;
  height: 100%;
  transform-origin: 47.5% 91%;
}

.bird__flip { transition: transform .25s ease; }

.bird__svg {
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
  transform-origin: 47.5% 91%;
  filter: drop-shadow(0 6px 5px rgba(76, 118, 89, .2));
}

.bird__torso { fill: #a9c9ea; }
.bird__tail { fill: #8fb3dc; }
.bird__belly { fill: #fcdcc6; }
.bird__cheek { fill: #f5b3b5; opacity: .85; }
.bird__beak { fill: #f4bd74; }
.bird__crest { fill: none; stroke: #8fb3dc; stroke-width: 3; stroke-linecap: round; }
.bird__wing-folded { fill: #8fb3dc; transition: opacity .15s; }
.bird__wing path { fill: #94b8df; }
.bird__wing--far path { fill: #7fa5d0; }

.bird__legs path {
  fill: none;
  stroke: #d9a074;
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.bird__legs {
  transform-box: view-box;
  transform-origin: 57px 74px;
  transition: opacity .2s, transform .2s;
}

.bird__wing {
  opacity: 0;
  transform-box: view-box;
  transform-origin: 62px 52px;
}

.bird__head {
  transform-box: view-box;
  transform-origin: 76px 50px;
}

.bird__eye {
  transform-box: fill-box;
  transform-origin: center;
  animation: blink 5s infinite;
}

/* Flying */
.is-flying .bird__wing { opacity: 1; animation: flap .2s ease-in-out infinite alternate; }
.is-flying .bird__wing--far { animation-delay: -.07s; }
.is-flying .bird__wing-folded { opacity: 0; }
.is-flying .bird__legs { opacity: 0; transform: scaleY(.3); }

/* Landing and perched */
.is-landing .bird__svg { animation: squash .4s ease-out; }
.is-perched .bird__svg { animation: breathe 3.2s ease-in-out infinite; }
.is-perched .bird__head { animation: look 7s ease-in-out infinite; }

@keyframes flap {
  from { transform: scaleY(1); }
  to { transform: scaleY(-.85); }
}

@keyframes blink {
  0%, 92%, 100% { transform: scaleY(1); }
  95% { transform: scaleY(.1); }
}

@keyframes squash {
  0% { transform: scale(1.08, .86); }
  55% { transform: scale(.96, 1.05); }
  100% { transform: none; }
}

@keyframes breathe {
  0%, 100% { transform: none; }
  50% { transform: scale(1.01, 1.03); }
}

@keyframes look {
  0%, 38%, 100% { transform: rotate(0); }
  44%, 58% { transform: rotate(-12deg); }
  64%, 80% { transform: rotate(7deg); }
}

/* A little song note while perched */
.bird__note {
  position: absolute;
  top: -12%;
  right: 4%;
  color: var(--sage-700);
  font-size: 1.15rem;
  opacity: 0;
}

.bird[data-face="left"] .bird__note { right: auto; left: 4%; }

.is-singing .bird__note { animation: note 1.6s ease-out; }
.bird[data-face="left"].is-singing .bird__note { animation-name: note-left; }

@keyframes note {
  0% { opacity: 0; transform: translate(0, 0) rotate(-10deg); }
  20% { opacity: 1; }
  100% { opacity: 0; transform: translate(12px, -28px) rotate(12deg); }
}

@keyframes note-left {
  0% { opacity: 0; transform: translate(0, 0) rotate(10deg); }
  20% { opacity: 1; }
  100% { opacity: 0; transform: translate(-12px, -28px) rotate(-12deg); }
}
</style>

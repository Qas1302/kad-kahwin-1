<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'

import { userMessage } from '../application/errors'
import type { WeddingEvent } from '../domain/event'
import BirdCompanion from './components/BirdCompanion.vue'
import SceneryBackground from './components/decor/SceneryBackground.vue'
import SvgSprite from './components/decor/SvgSprite.vue'
import DetailsSection from './components/sections/DetailsSection.vue'
import OpeningSection from './components/sections/OpeningSection.vue'
import RsvpSection from './components/sections/RsvpSection.vue'
import StepNav from './components/StepNav.vue'
import { prefersReducedMotion } from './composables/useReducedMotion'
import { useServices } from './composables/useServices'

const STEPS = ['Welcome', 'Details', 'RSVP'] as const
const TRANSITION_MS = 900

const { loadEvent } = useServices()

const event = ref<WeddingEvent | null>(null)
const loadError = ref('')
const current = ref(0)
const leaving = ref<number | null>(null)

const invite = ref<HTMLElement | null>(null)
const stage = ref<HTMLElement | null>(null)
const panels = ref<HTMLElement[]>([])
const bird = ref<InstanceType<typeof BirdCompanion> | null>(null)
let switching = false

const perchIn = (index: number) => panels.value[index]?.querySelector<HTMLElement>('.perch') ?? null

function setPanel(el: unknown, index: number) {
  if (el instanceof HTMLElement) panels.value[index] = el
}

function panelClass(index: number) {
  return { 'is-active': current.value === index, 'is-leaving': leaving.value === index }
}

function focusHeading(index: number) {
  panels.value[index]?.querySelector<HTMLElement>('[data-focus]')?.focus({ preventScroll: true })
}

function goTo(index: number) {
  const target = panels.value[index]
  if (switching || index === current.value || !target || !stage.value) return
  switching = true
  const reduced = prefersReducedMotion()

  // Set the slide direction and flush styles before the classes change,
  // so the incoming section starts on the correct side.
  stage.value.style.setProperty('--dir', index > current.value ? '1' : '-1')
  void target.offsetWidth

  leaving.value = current.value
  current.value = index

  // Bring the top of the card back into view if the guest scrolled down.
  const top = invite.value?.getBoundingClientRect().top ?? 0
  if (top < 0) window.scrollBy({ top: top - 8, behavior: reduced ? 'auto' : 'smooth' })

  nextTick(() => bird.value?.flyTo(perchIn(index)))

  window.setTimeout(
    () => {
      leaving.value = null
      switching = false
      focusHeading(index)
    },
    reduced ? 50 : TRANSITION_MS,
  )
}

async function followPerch() {
  await nextTick()
  bird.value?.flyTo(perchIn(current.value))
}

async function load() {
  loadError.value = ''
  try {
    event.value = await loadEvent()
    document.title = `${event.value.partnerOne} & ${event.value.partnerTwo} · Wedding Invitation`
    await nextTick()
    // Wait for web fonts so perch positions are final, then let the bird fly in.
    await document.fonts?.ready
    window.setTimeout(() => bird.value?.enter(perchIn(0)), prefersReducedMotion() ? 0 : 600)
  } catch (error) {
    loadError.value = userMessage(error)
  }
}

onMounted(load)
</script>

<template>
  <SvgSprite />
  <SceneryBackground />

  <main ref="invite" class="invite">
    <div v-if="loadError" class="card status" role="alert">
      <h1 class="title">We couldn't open the invitation</h1>
      <p>{{ loadError }}</p>
      <button type="button" class="btn btn--primary" @click="load">Try again</button>
    </div>

    <div v-else-if="!event" class="card status" role="status">
      <span class="spinner" aria-hidden="true" />
      <p>Preparing your invitation…</p>
    </div>

    <template v-else>
      <StepNav :steps="STEPS" :current="current" @select="goTo" />

      <div ref="stage" class="stage">
        <section
          :ref="(el) => setPanel(el, 0)"
          class="panel"
          :class="panelClass(0)"
          :inert="current !== 0"
          aria-labelledby="opening-title"
        >
          <OpeningSection :event="event" @next="goTo(1)" />
        </section>

        <section
          :ref="(el) => setPanel(el, 1)"
          class="panel"
          :class="panelClass(1)"
          :inert="current !== 1"
          aria-labelledby="details-title"
        >
          <DetailsSection :event="event" @back="goTo(0)" @next="goTo(2)" />
        </section>

        <section
          :ref="(el) => setPanel(el, 2)"
          class="panel"
          :class="panelClass(2)"
          :inert="current !== 2"
          aria-labelledby="rsvp-title"
        >
          <RsvpSection :event="event" @back="goTo(1)" @perch-change="followPerch" />
        </section>

        <BirdCompanion ref="bird" />
      </div>
    </template>
  </main>
</template>

<style scoped>
.invite {
  position: relative;
  z-index: 1;
  width: min(100% - 2rem, 600px);
  margin-inline: auto;
  padding: 1.5rem 0 5rem;
  animation: rise 1.1s cubic-bezier(.2, .8, .2, 1) both;
}

@keyframes rise {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: none; }
}

/* Sections are stacked; only the active one is in the document flow. */
.stage {
  --dir: 1;
  position: relative;
  margin-top: 4rem;
}

.panel {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  opacity: 0;
  visibility: hidden;
  transform: translateX(calc(var(--dir) * 48px)) scale(.97);
}

.panel.is-active {
  position: relative;
  opacity: 1;
  visibility: visible;
  transform: none;
  transition:
    opacity .7s ease .2s,
    transform .9s cubic-bezier(.22, .8, .24, 1) .2s;
}

.panel.is-leaving {
  visibility: visible;
  opacity: 0;
  transform: translateX(calc(var(--dir) * -48px)) scale(.97);
  transition: opacity .45s ease, transform .6s ease-in;
}

.status {
  margin-top: 4rem;
  color: var(--ink-soft);
  font-family: var(--font-serif);
  font-size: 1.25rem;
}

.status p { margin: .5rem 0 1.5rem; }

.spinner {
  display: inline-block;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 100% 0 100% 0;
  background: var(--sage-300);
  animation: sway 1.4s ease-in-out infinite alternate;
}

@keyframes sway {
  from { transform: rotate(-25deg) scale(.9); }
  to { transform: rotate(25deg) scale(1.05); }
}
</style>

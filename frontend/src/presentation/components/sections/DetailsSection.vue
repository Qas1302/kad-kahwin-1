<script setup lang="ts">
import { computed } from 'vue'

import type { WeddingEvent } from '../../../domain/event'
import { googleCalendarUrl } from '../../utils/calendar'
import { formatLongDate, formatTime } from '../../utils/format'
import AppIcon from '../AppIcon.vue'
import CountdownTimer from '../CountdownTimer.vue'
import LeafTwig from '../decor/LeafTwig.vue'

const props = defineProps<{ event: WeddingEvent }>()
defineEmits<{ next: []; back: [] }>()

const tz = computed(() => props.event.timezone)
const date = computed(() => formatLongDate(props.event.startsAt, tz.value))
const timeRange = computed(
  () => `${formatTime(props.event.startsAt, tz.value)} – ${formatTime(props.event.endsAt, tz.value)}`,
)
const calendarUrl = computed(() => googleCalendarUrl(props.event))
</script>

<template>
  <div class="card">
    <LeafTwig placement="left" face="right" />

    <p class="eyebrow">Save the date</p>
    <h2 id="details-title" class="title" tabindex="-1" data-focus>The Celebration</h2>

    <CountdownTimer :target="event.startsAt" />

    <ul class="details">
      <li class="detail">
        <span class="detail__icon"><AppIcon name="calendar" /></span>
        <div>
          <h3>When</h3>
          <p>{{ date }}<br>{{ timeRange }}</p>
        </div>
      </li>
      <li class="detail">
        <span class="detail__icon"><AppIcon name="pin" /></span>
        <div>
          <h3>Where</h3>
          <p>{{ event.venue.name }}<br>{{ event.venue.address }}</p>
          <a class="link" :href="event.venue.mapUrl" target="_blank" rel="noopener noreferrer">
            Open in Maps<span class="sr-only"> (opens in a new tab)</span>
          </a>
        </div>
      </li>
      <li class="detail">
        <span class="detail__icon"><AppIcon name="leaf" /></span>
        <div>
          <h3>Dress code</h3>
          <p>{{ event.dressCode }}</p>
        </div>
      </li>
    </ul>

    <template v-if="event.programme.length">
      <h3 class="subtitle">Programme</h3>
      <ol class="timeline">
        <li v-for="item in event.programme" :key="item.startsAt.toISOString() + item.title">
          <time :datetime="item.startsAt.toISOString()">{{ formatTime(item.startsAt, tz) }}</time>
          <span>{{ item.title }}</span>
        </li>
      </ol>
    </template>

    <div class="actions">
      <button type="button" class="btn btn--ghost" @click="$emit('back')">
        <AppIcon name="arrow-left" />
        Back
      </button>
      <a class="btn btn--ghost" :href="calendarUrl" target="_blank" rel="noopener noreferrer">
        <AppIcon name="calendar-plus" />
        Add to calendar<span class="sr-only"> (opens in a new tab)</span>
      </a>
      <button type="button" class="btn btn--primary" @click="$emit('next')">
        RSVP
        <AppIcon name="arrow-right" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.details {
  display: grid;
  gap: .9rem;
  margin: 0 0 2.25rem;
  padding: 0;
  list-style: none;
  text-align: left;
}

.detail {
  display: grid;
  grid-template-columns: 44px 1fr;
  align-items: start;
  gap: .9rem;
  padding: 1rem 1.1rem;
  border: 1px solid var(--sage-200);
  border-radius: 20px;
  background: rgba(255, 255, 255, .65);
}

.detail__icon {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--sage-100);
  color: var(--sage-700);
  font-size: 22px;
}

.detail h3 {
  margin: 0 0 .15rem;
  color: var(--sage-700);
  font: 700 .72rem/1.4 var(--font-sans);
  letter-spacing: .16em;
  text-transform: uppercase;
}

.detail p {
  margin: 0;
  font-family: var(--font-serif);
  font-size: 1.15rem;
  line-height: 1.35;
}

.link {
  display: inline-flex;
  margin-top: .4rem;
  color: var(--sage-700);
  font-size: .88rem;
  font-weight: 700;
  text-underline-offset: 3px;
}

.timeline {
  --line: 5.15rem;
  position: relative;
  max-width: 340px;
  margin: 0 auto 2.25rem;
  padding: 0;
  list-style: none;
  text-align: left;
}

.timeline::before {
  content: "";
  position: absolute;
  top: .9rem;
  bottom: .9rem;
  left: var(--line);
  border-left: 2px dotted var(--sage-300);
}

.timeline li {
  position: relative;
  display: grid;
  grid-template-columns: calc(var(--line) - .75rem) 1fr;
  gap: 1.5rem;
  align-items: center;
  padding: .4rem 0;
}

.timeline li::after {
  content: "";
  position: absolute;
  top: 50%;
  left: calc(var(--line) - 5px);
  width: 12px;
  height: 12px;
  margin-top: -6px;
  border: 2px solid #fff;
  border-radius: 50%;
  background: var(--blush-300);
}

.timeline time {
  color: var(--sage-700);
  font-size: .88rem;
  font-weight: 700;
  text-align: right;
}

.timeline span {
  font-family: var(--font-serif);
  font-size: 1.15rem;
}

@media (max-width: 420px) {
  .timeline { --line: 4.65rem; }
}
</style>

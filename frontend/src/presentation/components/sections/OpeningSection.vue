<script setup lang="ts">
import { computed } from 'vue'

import type { WeddingEvent } from '../../../domain/event'
import { dateBadge, formatLongDate } from '../../utils/format'
import AppIcon from '../AppIcon.vue'
import LeafBranch from '../decor/LeafBranch.vue'

const props = defineProps<{ event: WeddingEvent }>()
defineEmits<{ next: [] }>()

const badge = computed(() => dateBadge(props.event.startsAt, props.event.timezone))
const longDate = computed(() => formatLongDate(props.event.startsAt, props.event.timezone))
</script>

<template>
  <div class="card opening">
    <LeafBranch face="left" />

    <p class="eyebrow">{{ event.hostLine }}</p>
    <h1 id="opening-title" class="names" tabindex="-1" data-focus>
      {{ event.partnerOne }} <span class="amp">&amp;</span> {{ event.partnerTwo }}
    </h1>
    <p class="lead">{{ event.invitationMessage }}</p>

    <div class="date-badge" role="img" :aria-label="longDate">
      <span>{{ badge.weekday }}</span>
      <strong>{{ badge.day }}</strong>
      <span>{{ badge.monthYear }}</span>
    </div>
    <p class="place">{{ event.venue.address }}</p>

    <button type="button" class="btn btn--primary" @click="$emit('next')">
      Open invitation
      <AppIcon name="arrow-right" />
    </button>
  </div>
</template>

<style scoped>
.opening { padding-top: clamp(5.5rem, 15vw, 6.75rem); }

.names {
  margin: .25rem 0 1rem;
  color: #557a60;
  font-family: var(--font-script);
  font-size: clamp(3.2rem, 13vw, 5rem);
  font-weight: 400;
  line-height: 1.05;
}

.amp {
  display: block;
  color: var(--rose-600);
  font-size: .55em;
  line-height: 1.2;
}

.lead {
  max-width: 26ch;
  margin: 0 auto 1.75rem;
  color: var(--ink-soft);
  font-family: var(--font-serif);
  font-size: clamp(1.15rem, 3.6vw, 1.35rem);
  font-style: italic;
  line-height: 1.45;
}

.date-badge {
  display: inline-grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 1rem;
  margin-bottom: .75rem;
  font-family: var(--font-serif);
}

.date-badge span {
  padding-block: .35rem;
  border-block: 1px solid var(--sage-300);
  font-size: .95rem;
  font-weight: 600;
  letter-spacing: .16em;
  text-transform: uppercase;
}

.date-badge strong {
  color: var(--sage-700);
  font-size: 3.2rem;
  font-weight: 500;
  line-height: 1;
}

.place {
  margin: 0 0 2rem;
  color: var(--ink-soft);
  font-family: var(--font-serif);
  font-size: 1.2rem;
}

@media (max-width: 420px) {
  .date-badge { gap: .6rem; }
  .date-badge span { font-size: .8rem; letter-spacing: .12em; }
}
</style>

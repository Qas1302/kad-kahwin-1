<script lang="ts">
export type IconName =
  | 'arrow-left'
  | 'arrow-right'
  | 'calendar'
  | 'calendar-plus'
  | 'pin'
  | 'leaf'
  | 'heart'
  | 'cloud'
  | 'send'

const CALENDAR = 'M6.5 5h11a3 3 0 0 1 3 3v9.5a3 3 0 0 1-3 3h-11a3 3 0 0 1-3-3V8a3 3 0 0 1 3-3z'

const PATHS: Record<IconName, string[]> = {
  'arrow-left': ['M19 12H5M11 6l-6 6 6 6'],
  'arrow-right': ['M5 12h14M13 6l6 6-6 6'],
  calendar: [CALENDAR, 'M3.5 10h17M8 3v4M16 3v4'],
  'calendar-plus': [CALENDAR, 'M3.5 10h17M8 3v4M16 3v4M12 13v5M9.5 15.5h5'],
  pin: ['M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z', 'M14.5 9.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z'],
  leaf: ['M5 19c0-8 5-14 15-14 0 10-6 15-14 15', 'M5 19c3-4 6-7 10-9'],
  heart: ['M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z'],
  cloud: ['M7 18a4 4 0 0 1 .4-8 5 5 0 0 1 9.7 1.3A3.5 3.5 0 0 1 17 18z'],
  send: ['M4 12l16-8-6 16-3-7-7-1z'],
}
</script>

<script setup lang="ts">
defineProps<{ name: IconName }>()
</script>

<template>
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
    <path v-for="d in PATHS[name]" :key="d" :d="d" />
  </svg>
</template>

<script setup lang="ts">
defineProps<{ steps: readonly string[]; current: number }>()
defineEmits<{ select: [index: number] }>()
</script>

<template>
  <nav class="steps" aria-label="Invitation sections">
    <ol>
      <li v-for="(label, index) in steps" :key="label">
        <button
          type="button"
          class="steps__btn"
          :aria-current="index === current ? 'step' : undefined"
          @click="$emit('select', index)"
        >
          {{ label }}
        </button>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
ol {
  display: flex;
  justify-content: center;
  gap: .5rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.steps__btn {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  min-height: 40px;
  padding: .5rem 1rem;
  border: 1px solid rgba(255, 255, 255, .9);
  border-radius: 999px;
  background: rgba(255, 255, 255, .6);
  color: var(--ink-soft);
  font: 700 .82rem/1 var(--font-sans);
  letter-spacing: .05em;
  cursor: pointer;
  transition: background-color .3s, color .3s, transform .2s;
}

.steps__btn::before {
  content: "";
  width: .6rem;
  height: .6rem;
  border-radius: 100% 0 100% 0;
  background: var(--sage-300);
  transition: background-color .3s;
}

.steps__btn:hover { transform: translateY(-1px); background: rgba(255, 255, 255, .85); }

.steps__btn[aria-current="step"] {
  border-color: var(--sage-700);
  background: var(--sage-700);
  color: #fff;
}

.steps__btn[aria-current="step"]::before { background: var(--blush-300); }

@media (max-width: 420px) {
  .steps__btn { padding: .5rem .8rem; font-size: .78rem; }
}
</style>

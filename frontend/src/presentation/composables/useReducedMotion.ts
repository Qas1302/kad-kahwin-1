import { onBeforeUnmount, onMounted, ref, type Ref } from 'vue'

const QUERY = '(prefers-reduced-motion: reduce)'

export const prefersReducedMotion = (): boolean => window.matchMedia(QUERY).matches

export function useReducedMotion(): Ref<boolean> {
  const media = window.matchMedia(QUERY)
  const reduced = ref(media.matches)
  const update = (event: MediaQueryListEvent) => {
    reduced.value = event.matches
  }

  onMounted(() => media.addEventListener('change', update))
  onBeforeUnmount(() => media.removeEventListener('change', update))
  return reduced
}

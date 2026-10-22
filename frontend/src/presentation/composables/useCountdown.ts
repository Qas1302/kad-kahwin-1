import { computed, onBeforeUnmount, onMounted, ref, toValue, type MaybeRefOrGetter } from 'vue'

const pad = (n: number) => String(n).padStart(2, '0')

export function useCountdown(target: MaybeRefOrGetter<Date>) {
  const now = ref(Date.now())
  let timer: number | undefined

  onMounted(() => {
    timer = window.setInterval(() => {
      now.value = Date.now()
    }, 1000)
  })
  onBeforeUnmount(() => window.clearInterval(timer))

  return computed(() => {
    const total = Math.max(0, Math.floor((toValue(target).getTime() - now.value) / 1000))
    return {
      done: total === 0,
      days: pad(Math.floor(total / 86400)),
      hours: pad(Math.floor((total % 86400) / 3600)),
      minutes: pad(Math.floor((total % 3600) / 60)),
      seconds: pad(total % 60),
    }
  })
}

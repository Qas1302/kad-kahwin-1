<script setup lang="ts">
import { computed, nextTick, onMounted, reactive, ref } from 'vue'

import { RsvpValidationError, userMessage } from '../../../application/errors'
import type { WeddingEvent } from '../../../domain/event'
import {
  draftFromRsvp,
  emptyDraft,
  firstName,
  RSVP_LIMITS,
  type Rsvp,
  type RsvpErrors,
  type RsvpField,
} from '../../../domain/rsvp'
import { useServices } from '../../composables/useServices'
import { formatDayMonthYear } from '../../utils/format'
import AppIcon from '../AppIcon.vue'
import LeafTwig from '../decor/LeafTwig.vue'

const props = defineProps<{ event: WeddingEvent }>()
/** `perch-change` fires when the visible perch moves (form <-> thank-you), so the bird can follow. */
const emit = defineEmits<{ back: []; 'perch-change': [] }>()

const { submitRsvp, restoreRsvp } = useServices()

const draft = reactive(emptyDraft())
const errors = ref<RsvpErrors>({})
const formError = ref('')
const submitting = ref(false)
const saved = ref<Rsvp | null>(null)
const editing = ref(false)

const nameInput = ref<HTMLInputElement | null>(null)
const phoneInput = ref<HTMLInputElement | null>(null)
const attendingInput = ref<HTMLInputElement | null>(null)
const guestsSelect = ref<HTMLSelectElement | null>(null)
const messageInput = ref<HTMLTextAreaElement | null>(null)
const thanksTitle = ref<HTMLElement | null>(null)

const showThanks = computed(() => saved.value !== null && !editing.value)
const deadline = computed(() => formatDayMonthYear(props.event.rsvpDeadline, props.event.timezone))
const guestOptions = computed(() => Array.from({ length: props.event.maxGuestsPerRsvp }, (_, i) => i + 1))

const thanksCopy = computed(() => {
  const rsvp = saved.value
  if (!rsvp) return { title: '', message: '' }
  const name = firstName(rsvp.guestName)
  if (rsvp.attendance === 'attending') {
    const seats = rsvp.guestCount > 1 ? `${rsvp.guestCount} seats` : 'a seat'
    return {
      title: 'See you there',
      message: `Thank you, ${name}. We've saved ${seats} for you and can't wait to celebrate together.`,
    }
  }
  return {
    title: 'Thank you',
    message: `Thank you for letting us know, ${name}. You'll be missed, and we're grateful for your love and wishes.`,
  }
})

function clearError(field: RsvpField) {
  if (errors.value[field]) errors.value = { ...errors.value, [field]: undefined }
}

function focusFirstInvalid() {
  const order: [RsvpField, HTMLElement | null][] = [
    ['guestName', nameInput.value],
    ['phone', phoneInput.value],
    ['attendance', attendingInput.value],
    ['guestCount', guestsSelect.value],
    ['message', messageInput.value],
  ]
  order.find(([field]) => errors.value[field])?.[1]?.focus()
}

async function onSubmit() {
  formError.value = ''
  submitting.value = true
  try {
    saved.value = await submitRsvp({ ...draft }, props.event)
    errors.value = {}
    editing.value = false
    await nextTick()
    thanksTitle.value?.focus({ preventScroll: true })
    emit('perch-change')
  } catch (error) {
    if (error instanceof RsvpValidationError) {
      errors.value = error.errors
      await nextTick()
      focusFirstInvalid()
    } else {
      formError.value = userMessage(error)
    }
  } finally {
    submitting.value = false
  }
}

async function editResponse() {
  editing.value = true
  await nextTick()
  nameInput.value?.focus({ preventScroll: true })
  emit('perch-change')
}

onMounted(async () => {
  const previous = await restoreRsvp()
  if (previous) {
    Object.assign(draft, draftFromRsvp(previous))
    saved.value = previous
  }
})
</script>

<template>
  <div class="card">
    <LeafTwig v-if="!showThanks" placement="right" face="left" />

    <!-- Thank-you state -->
    <div v-if="showThanks" class="thanks">
      <LeafTwig placement="center" face="right" />
      <h2 id="rsvp-title" ref="thanksTitle" class="title" tabindex="-1" data-focus>{{ thanksCopy.title }}</h2>
      <p>{{ thanksCopy.message }}</p>
      <button v-if="event.rsvpOpen" type="button" class="btn btn--ghost" @click="editResponse">
        Change my response
      </button>
    </div>

    <!-- RSVPs closed -->
    <div v-else-if="!event.rsvpOpen" class="closed">
      <p class="eyebrow">RSVP</p>
      <h2 id="rsvp-title" class="title" tabindex="-1" data-focus>Replies are closed</h2>
      <p>The RSVP deadline was {{ deadline }}. Please contact the couple directly if your plans have changed.</p>
    </div>

    <!-- Form -->
    <template v-else>
      <p class="eyebrow">Kindly reply by {{ deadline }}</p>
      <h2 id="rsvp-title" class="title" tabindex="-1" data-focus>Will you join us?</h2>

      <form class="rsvp" novalidate @submit.prevent="onSubmit">
        <div class="field">
          <label class="field__label" for="rsvp-name">Full name</label>
          <input
            id="rsvp-name"
            ref="nameInput"
            v-model="draft.guestName"
            class="input"
            name="guestName"
            type="text"
            autocomplete="name"
            :maxlength="RSVP_LIMITS.nameMax"
            required
            :aria-invalid="!!errors.guestName"
            aria-describedby="rsvp-name-error"
            @input="clearError('guestName')"
          >
          <p id="rsvp-name-error" class="field__error">{{ errors.guestName }}</p>
        </div>

        <div class="field">
          <label class="field__label" for="rsvp-phone">Phone number <span class="optional">(optional)</span></label>
          <input
            id="rsvp-phone"
            ref="phoneInput"
            v-model="draft.phone"
            class="input"
            name="phone"
            type="tel"
            autocomplete="tel"
            inputmode="tel"
            :maxlength="RSVP_LIMITS.phoneMax"
            :aria-invalid="!!errors.phone"
            aria-describedby="rsvp-phone-error"
            @input="clearError('phone')"
          >
          <p id="rsvp-phone-error" class="field__error">{{ errors.phone }}</p>
        </div>

        <fieldset class="field">
          <legend class="field__label">Will you be attending?</legend>
          <div class="choices">
            <div class="choice">
              <input
                id="attending-yes"
                ref="attendingInput"
                v-model="draft.attendance"
                type="radio"
                name="attendance"
                value="attending"
                required
                :aria-invalid="!!errors.attendance"
                aria-describedby="rsvp-attendance-error"
                @change="clearError('attendance')"
              >
              <label for="attending-yes"><AppIcon name="heart" class="choice__icon" />Joyfully accept</label>
            </div>
            <div class="choice choice--no">
              <input
                id="attending-no"
                v-model="draft.attendance"
                type="radio"
                name="attendance"
                value="declined"
                :aria-invalid="!!errors.attendance"
                aria-describedby="rsvp-attendance-error"
                @change="clearError('attendance')"
              >
              <label for="attending-no"><AppIcon name="cloud" class="choice__icon" />Regretfully decline</label>
            </div>
          </div>
          <p id="rsvp-attendance-error" class="field__error">{{ errors.attendance }}</p>
        </fieldset>

        <div v-if="draft.attendance === 'attending'" class="field">
          <label class="field__label" for="rsvp-guests">
            Number of guests <span class="optional">(including you)</span>
          </label>
          <select
            id="rsvp-guests"
            ref="guestsSelect"
            v-model.number="draft.guestCount"
            class="input"
            name="guestCount"
            :aria-invalid="!!errors.guestCount"
            aria-describedby="rsvp-guests-error"
            @change="clearError('guestCount')"
          >
            <option v-for="n in guestOptions" :key="n" :value="n">{{ n }}</option>
          </select>
          <p id="rsvp-guests-error" class="field__error">{{ errors.guestCount }}</p>
        </div>

        <div class="field">
          <label class="field__label" for="rsvp-message">
            Wishes for the couple <span class="optional">(optional)</span>
          </label>
          <textarea
            id="rsvp-message"
            ref="messageInput"
            v-model="draft.message"
            class="input"
            name="message"
            rows="4"
            :maxlength="RSVP_LIMITS.messageMax"
            :aria-invalid="!!errors.message"
            aria-describedby="rsvp-message-count rsvp-message-error"
            @input="clearError('message')"
          />
          <p id="rsvp-message-count" class="field__hint">{{ draft.message.length }} / {{ RSVP_LIMITS.messageMax }}</p>
          <p id="rsvp-message-error" class="field__error">{{ errors.message }}</p>
        </div>

        <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>

        <button type="submit" class="btn btn--primary btn--block" :disabled="submitting">
          <template v-if="submitting">Sending…</template>
          <template v-else>Send RSVP <AppIcon name="send" /></template>
        </button>
      </form>
    </template>

    <div class="actions footer">
      <button type="button" class="btn btn--ghost" @click="$emit('back')">
        <AppIcon name="arrow-left" />
        Back to details
      </button>
    </div>
  </div>
</template>

<style scoped>
.rsvp {
  display: grid;
  gap: 1.1rem;
  margin-top: 1.5rem;
  text-align: left;
}

fieldset.field {
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
}

.field__label {
  display: block;
  margin-bottom: .4rem;
  padding: 0;
  color: var(--ink);
  font-size: .92rem;
  font-weight: 700;
}

.optional { color: var(--ink-soft); font-weight: 400; }

.input {
  width: 100%;
  padding: .8rem 1rem;
  border: 1.5px solid var(--sage-200);
  border-radius: 14px;
  background: rgba(255, 255, 255, .9);
  color: var(--ink);
  font: 400 1rem/1.4 var(--font-sans);
  transition: border-color .2s, box-shadow .2s;
}

.input:hover { border-color: var(--sage-300); }

.input:focus {
  outline: none;
  border-color: var(--sage-500);
  box-shadow: 0 0 0 4px rgba(127, 169, 139, .3);
}

.input[aria-invalid="true"] { border-color: var(--error); }

textarea.input { min-height: 6rem; resize: vertical; }

select.input {
  padding-right: 2.75rem;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234c7659' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-position: right 1rem center;
  background-repeat: no-repeat;
  background-size: 18px;
}

.choices {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: .75rem;
}

.choice { position: relative; }

.choice input {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  opacity: 0;
  cursor: pointer;
}

.choice label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: .4rem;
  height: 100%;
  padding: 1rem .75rem;
  border: 1.5px solid var(--sage-200);
  border-radius: 18px;
  background: rgba(255, 255, 255, .8);
  font-weight: 700;
  text-align: center;
  transition: border-color .2s, background-color .2s, box-shadow .2s, transform .2s;
}

.choice__icon { width: 1.6rem; height: 1.6rem; color: var(--sage-700); }
.choice--no .choice__icon { color: var(--rose-600); }

.choice input:hover + label { transform: translateY(-1px); border-color: var(--sage-300); }

.choice input:checked + label {
  border-color: var(--sage-500);
  background: var(--sage-100);
  box-shadow: 0 0 0 3px rgba(127, 169, 139, .25);
}

.choice--no input:checked + label {
  border-color: #d79aa2;
  background: var(--blush-100);
  box-shadow: 0 0 0 3px rgba(244, 199, 204, .45);
}

.choice input:focus-visible + label {
  outline: 3px solid var(--sage-700);
  outline-offset: 2px;
}

.choice input[aria-invalid="true"] + label { border-color: var(--error); }

.field__error {
  margin: .35rem 0 0;
  color: var(--error);
  font-size: .85rem;
  font-weight: 600;
}

.field__error:empty { display: none; }

.field__hint {
  margin: .3rem 0 0;
  color: var(--ink-soft);
  font-size: .8rem;
  text-align: right;
}

.form-error {
  margin: 0;
  padding: .75rem 1rem;
  border-radius: 12px;
  background: var(--blush-100);
  color: var(--error);
  font-weight: 600;
}

.thanks { padding: 2rem 0 .5rem; }

.thanks p,
.closed p {
  max-width: 30ch;
  margin: .5rem auto 1.5rem;
  color: var(--ink-soft);
  font-family: var(--font-serif);
  font-size: 1.3rem;
  line-height: 1.45;
}

.footer { margin-top: 1.5rem; }

@media (max-width: 420px) {
  .choices { grid-template-columns: 1fr; }
}
</style>

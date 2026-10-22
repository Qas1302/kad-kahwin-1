/**
 * RSVP rules shared by the UI. They mirror the backend domain so guests get instant feedback;
 * the backend remains the source of truth.
 */

export type Attendance = 'attending' | 'declined'

export type RsvpField = 'guestName' | 'phone' | 'attendance' | 'guestCount' | 'message'

export type RsvpErrors = Partial<Record<RsvpField, string>>

/** What the guest is typing into the form. */
export interface RsvpDraft {
  guestName: string
  phone: string
  attendance: Attendance | null
  guestCount: number
  message: string
}

/** A validated, normalised answer ready to be sent. */
export interface RsvpSubmission {
  guestName: string
  phone: string | null
  attendance: Attendance
  guestCount: number
  message: string | null
}

/** An RSVP the backend has stored. */
export interface Rsvp extends RsvpSubmission {
  id: string
  updatedAt: Date
}

export const RSVP_LIMITS = {
  nameMin: 2,
  nameMax: 80,
  phoneMax: 20,
  messageMax: 300,
} as const

const PHONE_PATTERN = /^\+?[\d\s()-]{7,20}$/

const RSVP_FIELDS: readonly RsvpField[] = ['guestName', 'phone', 'attendance', 'guestCount', 'message']

export const isRsvpField = (value: unknown): value is RsvpField =>
  typeof value === 'string' && (RSVP_FIELDS as readonly string[]).includes(value)

export function emptyDraft(): RsvpDraft {
  return { guestName: '', phone: '', attendance: null, guestCount: 1, message: '' }
}

export function draftFromRsvp(rsvp: Rsvp): RsvpDraft {
  return {
    guestName: rsvp.guestName,
    phone: rsvp.phone ?? '',
    attendance: rsvp.attendance,
    guestCount: Math.max(1, rsvp.guestCount),
    message: rsvp.message ?? '',
  }
}

export function validateRsvp(draft: RsvpDraft, maxGuests: number): RsvpErrors {
  const errors: RsvpErrors = {}
  const name = draft.guestName.trim()
  const phone = draft.phone.trim()

  if (name.length < RSVP_LIMITS.nameMin || name.length > RSVP_LIMITS.nameMax) {
    errors.guestName = 'Please enter your name.'
  }
  if (phone && !PHONE_PATTERN.test(phone)) {
    errors.phone = 'Please enter a valid phone number.'
  }
  if (!draft.attendance) {
    errors.attendance = 'Please let us know if you can make it.'
  }
  if (draft.attendance === 'attending' && (draft.guestCount < 1 || draft.guestCount > maxGuests)) {
    errors.guestCount = `Please choose between 1 and ${maxGuests} guests.`
  }
  if (draft.message.trim().length > RSVP_LIMITS.messageMax) {
    errors.message = `Please keep your message under ${RSVP_LIMITS.messageMax} characters.`
  }
  return errors
}

/** Call only after validateRsvp returned no errors. */
export function toSubmission(draft: RsvpDraft): RsvpSubmission {
  if (!draft.attendance) throw new Error('Cannot submit an RSVP without attendance')
  const attending = draft.attendance === 'attending'
  return {
    guestName: draft.guestName.trim().replace(/\s+/g, ' '),
    phone: draft.phone.trim() || null,
    attendance: draft.attendance,
    guestCount: attending ? draft.guestCount : 0,
    message: draft.message.trim() || null,
  }
}

export const firstName = (fullName: string): string => fullName.trim().split(/\s+/)[0] ?? fullName

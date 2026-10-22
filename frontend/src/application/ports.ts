/** Interfaces the use cases depend on. Implemented in src/infrastructure. */

import type { WeddingEvent } from '../domain/event'
import type { Rsvp, RsvpSubmission } from '../domain/rsvp'

/** Proof that this browser created an RSVP, so the guest can change it later. */
export interface RsvpReceipt {
  id: string
  editToken: string
}

export interface EventGateway {
  fetchEvent(): Promise<WeddingEvent>
}

export interface RsvpGateway {
  create(submission: RsvpSubmission): Promise<{ rsvp: Rsvp; editToken: string }>
  replace(receipt: RsvpReceipt, submission: RsvpSubmission): Promise<Rsvp>
  fetch(receipt: RsvpReceipt): Promise<Rsvp>
}

export interface ReceiptStore {
  load(): RsvpReceipt | null
  save(receipt: RsvpReceipt): void
  clear(): void
}

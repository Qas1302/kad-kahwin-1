import type { WeddingEvent } from '../domain/event'
import { isRsvpField, toSubmission, validateRsvp, type Rsvp, type RsvpDraft } from '../domain/rsvp'
import { GatewayError, RsvpValidationError } from './errors'
import type { EventGateway, ReceiptStore, RsvpGateway } from './ports'

export interface AppServices {
  loadEvent(): Promise<WeddingEvent>
  /** Saves the guest's answer, updating their previous one if this browser sent it. */
  submitRsvp(draft: RsvpDraft, event: WeddingEvent): Promise<Rsvp>
  /** The answer this browser sent earlier, if it still exists. */
  restoreRsvp(): Promise<Rsvp | null>
}

export interface AppDependencies {
  events: EventGateway
  rsvps: RsvpGateway
  receipts: ReceiptStore
}

export function createAppServices({ events, rsvps, receipts }: AppDependencies): AppServices {
  return {
    loadEvent: () => events.fetchEvent(),

    async submitRsvp(draft, event) {
      const errors = validateRsvp(draft, event.maxGuestsPerRsvp)
      if (Object.keys(errors).length > 0) throw new RsvpValidationError(errors)
      const submission = toSubmission(draft)

      try {
        const receipt = receipts.load()
        if (receipt) {
          try {
            return await rsvps.replace(receipt, submission)
          } catch (error) {
            if (!(error instanceof GatewayError && error.isStaleReceipt)) throw error
            receipts.clear() // fall through and create a fresh RSVP
          }
        }

        const { rsvp, editToken } = await rsvps.create(submission)
        receipts.save({ id: rsvp.id, editToken })
        return rsvp
      } catch (error) {
        // Surface server-side field errors next to the matching input.
        if (error instanceof GatewayError && error.status === 422 && isRsvpField(error.field)) {
          throw new RsvpValidationError({ [error.field]: error.message })
        }
        throw error
      }
    },

    async restoreRsvp() {
      const receipt = receipts.load()
      if (!receipt) return null
      try {
        return await rsvps.fetch(receipt)
      } catch (error) {
        if (error instanceof GatewayError && error.isStaleReceipt) receipts.clear()
        return null
      }
    },
  }
}

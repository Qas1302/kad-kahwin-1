import type { ReceiptStore, RsvpReceipt } from '../../application/ports'

const KEY = 'wedding-rsvp-receipt'

/** Keeps the RSVP id and edit token in localStorage. Storage can be blocked, so every call is guarded. */
export class LocalReceiptStore implements ReceiptStore {
  private readonly storage: () => Storage

  constructor(storage: () => Storage = () => window.localStorage) {
    this.storage = storage
  }

  load(): RsvpReceipt | null {
    try {
      const value: unknown = JSON.parse(this.storage().getItem(KEY) ?? 'null')
      if (
        value &&
        typeof value === 'object' &&
        typeof (value as RsvpReceipt).id === 'string' &&
        typeof (value as RsvpReceipt).editToken === 'string'
      ) {
        const { id, editToken } = value as RsvpReceipt
        return { id, editToken }
      }
    } catch {
      /* unreadable or unavailable */
    }
    return null
  }

  save(receipt: RsvpReceipt): void {
    try {
      this.storage().setItem(KEY, JSON.stringify(receipt))
    } catch {
      /* the RSVP is still saved on the server; it just can't be edited from this browser */
    }
  }

  clear(): void {
    try {
      this.storage().removeItem(KEY)
    } catch {
      /* ignore */
    }
  }
}

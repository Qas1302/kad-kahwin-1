import type { RsvpErrors } from '../domain/rsvp'

/** The RSVP failed validation, either in the browser or on the server. */
export class RsvpValidationError extends Error {
  readonly errors: RsvpErrors

  constructor(errors: RsvpErrors) {
    super('The RSVP has invalid fields')
    this.name = 'RsvpValidationError'
    this.errors = errors
  }
}

/** A gateway (API) call failed. `message` is safe to show to guests. */
export class GatewayError extends Error {
  readonly code: string
  readonly status: number
  readonly field: string | undefined

  constructor(message: string, options: { code: string; status: number; field?: string }) {
    super(message)
    this.name = 'GatewayError'
    this.code = options.code
    this.status = options.status
    this.field = options.field
  }

  /** The record is gone or the stored token no longer matches it. */
  get isStaleReceipt(): boolean {
    return this.status === 403 || this.status === 404
  }
}

export function userMessage(error: unknown): string {
  return error instanceof GatewayError ? error.message : 'Something went wrong. Please try again.'
}

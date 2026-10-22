import { GatewayError } from '../../application/errors'
import type { RsvpGateway, RsvpReceipt } from '../../application/ports'
import type { Attendance, Rsvp, RsvpField, RsvpSubmission } from '../../domain/rsvp'
import type { HttpClient } from './httpClient'

interface RsvpRequestDto {
  guest_name: string
  phone: string | null
  attendance: Attendance
  guest_count: number
  message: string | null
}

interface RsvpDto extends RsvpRequestDto {
  id: string
  created_at: string
  updated_at: string
}

interface RsvpCreatedDto extends RsvpDto {
  edit_token: string
}

const FIELD_NAMES: Record<string, RsvpField> = {
  guest_name: 'guestName',
  phone: 'phone',
  attendance: 'attendance',
  guest_count: 'guestCount',
  message: 'message',
}

const toRequest = (s: RsvpSubmission): RsvpRequestDto => ({
  guest_name: s.guestName,
  phone: s.phone,
  attendance: s.attendance,
  guest_count: s.guestCount,
  message: s.message,
})

const toRsvp = (dto: RsvpDto): Rsvp => ({
  id: dto.id,
  guestName: dto.guest_name,
  phone: dto.phone,
  attendance: dto.attendance,
  guestCount: dto.guest_count,
  message: dto.message,
  updatedAt: new Date(dto.updated_at),
})

const tokenHeader = (receipt: RsvpReceipt) => ({ 'X-Rsvp-Token': receipt.editToken })

export class HttpRsvpGateway implements RsvpGateway {
  private readonly http: HttpClient

  constructor(http: HttpClient) {
    this.http = http
  }

  async create(submission: RsvpSubmission) {
    const dto = await this.call(() =>
      this.http.request<RsvpCreatedDto>('/rsvps', { method: 'POST', body: toRequest(submission) }),
    )
    return { rsvp: toRsvp(dto), editToken: dto.edit_token }
  }

  async replace(receipt: RsvpReceipt, submission: RsvpSubmission) {
    const dto = await this.call(() =>
      this.http.request<RsvpDto>(`/rsvps/${encodeURIComponent(receipt.id)}`, {
        method: 'PUT',
        body: toRequest(submission),
        headers: tokenHeader(receipt),
      }),
    )
    return toRsvp(dto)
  }

  async fetch(receipt: RsvpReceipt) {
    const dto = await this.call(() =>
      this.http.request<RsvpDto>(`/rsvps/${encodeURIComponent(receipt.id)}`, { headers: tokenHeader(receipt) }),
    )
    return toRsvp(dto)
  }

  /** Translate API field names (snake_case) into domain field names. */
  private async call<T>(request: () => Promise<T>): Promise<T> {
    try {
      return await request()
    } catch (error) {
      if (error instanceof GatewayError && error.field) {
        throw new GatewayError(error.message, {
          code: error.code,
          status: error.status,
          field: FIELD_NAMES[error.field] ?? error.field,
        })
      }
      throw error
    }
  }
}

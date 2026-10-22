import type { EventGateway } from '../../application/ports'
import type { WeddingEvent } from '../../domain/event'
import type { HttpClient } from './httpClient'

/** Shape returned by GET /event (snake_case, ISO dates). */
interface EventDto {
  partner_one: string
  partner_two: string
  host_line: string
  invitation_message: string
  starts_at: string
  ends_at: string
  timezone: string
  venue: { name: string; address: string; map_url: string }
  dress_code: string
  rsvp_deadline: string
  rsvp_open: boolean
  max_guests_per_rsvp: number
  programme: { starts_at: string; title: string }[]
}

const toEvent = (dto: EventDto): WeddingEvent => ({
  partnerOne: dto.partner_one,
  partnerTwo: dto.partner_two,
  hostLine: dto.host_line,
  invitationMessage: dto.invitation_message,
  startsAt: new Date(dto.starts_at),
  endsAt: new Date(dto.ends_at),
  timezone: dto.timezone,
  venue: { name: dto.venue.name, address: dto.venue.address, mapUrl: dto.venue.map_url },
  dressCode: dto.dress_code,
  rsvpDeadline: new Date(dto.rsvp_deadline),
  rsvpOpen: dto.rsvp_open,
  maxGuestsPerRsvp: dto.max_guests_per_rsvp,
  programme: dto.programme.map((item) => ({ startsAt: new Date(item.starts_at), title: item.title })),
})

export class HttpEventGateway implements EventGateway {
  private readonly http: HttpClient

  constructor(http: HttpClient) {
    this.http = http
  }

  async fetchEvent(): Promise<WeddingEvent> {
    return toEvent(await this.http.request<EventDto>('/event'))
  }
}

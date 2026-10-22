export interface Venue {
  name: string
  address: string
  mapUrl: string
}

export interface ProgrammeItem {
  startsAt: Date
  title: string
}

export interface WeddingEvent {
  partnerOne: string
  partnerTwo: string
  hostLine: string
  invitationMessage: string
  startsAt: Date
  endsAt: Date
  /** IANA time zone the event takes place in, used for displaying times. */
  timezone: string
  venue: Venue
  dressCode: string
  rsvpDeadline: Date
  rsvpOpen: boolean
  maxGuestsPerRsvp: number
  programme: ProgrammeItem[]
}

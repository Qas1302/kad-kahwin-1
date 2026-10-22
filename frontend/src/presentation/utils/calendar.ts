import type { WeddingEvent } from '../../domain/event'

const utcStamp = (date: Date) => date.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')

export function googleCalendarUrl(event: WeddingEvent): string {
  const params = new URLSearchParams({
    action: 'TEMPLATE',
    text: `Wedding of ${event.partnerOne} & ${event.partnerTwo}`,
    dates: `${utcStamp(event.startsAt)}/${utcStamp(event.endsAt)}`,
    location: `${event.venue.name}, ${event.venue.address}`,
    details: "We can't wait to celebrate with you.",
  })
  return `https://calendar.google.com/calendar/render?${params}`
}

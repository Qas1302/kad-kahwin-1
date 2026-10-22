from dataclasses import dataclass
from datetime import datetime

from app.domain.exceptions import InvalidRsvpError, RsvpClosedError


@dataclass(frozen=True, slots=True)
class Venue:
    name: str
    address: str
    map_url: str


@dataclass(frozen=True, slots=True)
class ProgrammeItem:
    starts_at: datetime
    title: str


@dataclass(frozen=True, slots=True)
class WeddingEvent:
    partner_one: str
    partner_two: str
    host_line: str
    invitation_message: str
    starts_at: datetime
    ends_at: datetime
    timezone: str
    venue: Venue
    dress_code: str
    rsvp_deadline: datetime
    max_guests_per_rsvp: int
    programme: tuple[ProgrammeItem, ...]

    def is_rsvp_open(self, now: datetime) -> bool:
        return now <= self.rsvp_deadline

    def ensure_rsvp_open(self, now: datetime) -> None:
        if not self.is_rsvp_open(now):
            raise RsvpClosedError("Sorry, the RSVP deadline has passed.")

    def ensure_guest_count_allowed(self, guest_count: int) -> None:
        if guest_count > self.max_guests_per_rsvp:
            raise InvalidRsvpError(
                f"Each RSVP can include up to {self.max_guests_per_rsvp} guests.",
                field="guest_count",
            )

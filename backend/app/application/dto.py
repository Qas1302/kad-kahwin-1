from dataclasses import dataclass

from app.domain.entities import Attendance, Rsvp, WeddingEvent


@dataclass(frozen=True, slots=True)
class RsvpInput:
    guest_name: str
    attendance: Attendance
    guest_count: int
    phone: str | None = None
    message: str | None = None


@dataclass(frozen=True, slots=True)
class EventOverview:
    event: WeddingEvent
    rsvp_open: bool


@dataclass(frozen=True, slots=True)
class SubmittedRsvp:
    rsvp: Rsvp
    # Returned once so the guest can change their answer later. Only its hash is stored.
    edit_token: str


@dataclass(frozen=True, slots=True)
class RsvpSummary:
    total_responses: int
    attending_responses: int
    declined_responses: int
    total_guests: int


@dataclass(frozen=True, slots=True)
class RsvpReport:
    summary: RsvpSummary
    rsvps: list[Rsvp]

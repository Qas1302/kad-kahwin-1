from uuid import UUID

from app.application.dto import RsvpInput, SubmittedRsvp
from app.application.ports import Clock, EventRepository, RsvpRepository, TokenService
from app.domain.entities import Rsvp, RsvpDetails
from app.domain.exceptions import RsvpAccessDeniedError, RsvpNotFoundError


def _to_details(data: RsvpInput) -> RsvpDetails:
    return RsvpDetails(
        guest_name=data.guest_name,
        attendance=data.attendance,
        guest_count=data.guest_count,
        phone=data.phone,
        message=data.message,
    )


def _load_owned(rsvps: RsvpRepository, tokens: TokenService, rsvp_id: UUID, edit_token: str) -> Rsvp:
    rsvp = rsvps.get(rsvp_id)
    if rsvp is None:
        raise RsvpNotFoundError("We couldn't find that RSVP.")
    if not tokens.verify(edit_token, rsvp.edit_token_hash):
        raise RsvpAccessDeniedError("You're not allowed to view or change this RSVP.")
    return rsvp


class SubmitRsvp:
    def __init__(
        self,
        events: EventRepository,
        rsvps: RsvpRepository,
        tokens: TokenService,
        clock: Clock,
    ) -> None:
        self._events = events
        self._rsvps = rsvps
        self._tokens = tokens
        self._clock = clock

    def execute(self, data: RsvpInput) -> SubmittedRsvp:
        now = self._clock.now()
        event = self._events.get()
        event.ensure_rsvp_open(now)

        details = _to_details(data)
        event.ensure_guest_count_allowed(details.guest_count)

        token = self._tokens.generate()
        rsvp = Rsvp.create(details, edit_token_hash=self._tokens.hash(token), now=now)
        self._rsvps.add(rsvp)
        return SubmittedRsvp(rsvp=rsvp, edit_token=token)


class UpdateRsvp:
    def __init__(
        self,
        events: EventRepository,
        rsvps: RsvpRepository,
        tokens: TokenService,
        clock: Clock,
    ) -> None:
        self._events = events
        self._rsvps = rsvps
        self._tokens = tokens
        self._clock = clock

    def execute(self, rsvp_id: UUID, edit_token: str, data: RsvpInput) -> Rsvp:
        now = self._clock.now()
        event = self._events.get()
        event.ensure_rsvp_open(now)

        existing = _load_owned(self._rsvps, self._tokens, rsvp_id, edit_token)
        details = _to_details(data)
        event.ensure_guest_count_allowed(details.guest_count)

        revised = existing.revise(details, now=now)
        self._rsvps.update(revised)
        return revised


class GetRsvp:
    def __init__(self, rsvps: RsvpRepository, tokens: TokenService) -> None:
        self._rsvps = rsvps
        self._tokens = tokens

    def execute(self, rsvp_id: UUID, edit_token: str) -> Rsvp:
        return _load_owned(self._rsvps, self._tokens, rsvp_id, edit_token)

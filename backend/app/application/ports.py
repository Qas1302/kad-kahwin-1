"""Interfaces the use cases depend on. Implemented in the infrastructure layer."""

from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.entities import Rsvp, WeddingEvent


class EventRepository(Protocol):
    def get(self) -> WeddingEvent: ...


class RsvpRepository(Protocol):
    def add(self, rsvp: Rsvp) -> None: ...

    def update(self, rsvp: Rsvp) -> None: ...

    def get(self, rsvp_id: UUID) -> Rsvp | None: ...

    def list_all(self) -> list[Rsvp]: ...


class TokenService(Protocol):
    def generate(self) -> str: ...

    def hash(self, token: str) -> str: ...

    def verify(self, token: str, token_hash: str) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...

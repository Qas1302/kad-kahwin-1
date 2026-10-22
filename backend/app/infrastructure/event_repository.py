import json
from datetime import datetime
from functools import cached_property
from pathlib import Path

from app.domain.entities import ProgrammeItem, Venue, WeddingEvent


class JsonEventRepository:
    """Reads the event details from a JSON file so the couple can edit them without code."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def get(self) -> WeddingEvent:
        return self._event

    @cached_property
    def _event(self) -> WeddingEvent:
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        return WeddingEvent(
            partner_one=raw["partner_one"],
            partner_two=raw["partner_two"],
            host_line=raw["host_line"],
            invitation_message=raw["invitation_message"],
            starts_at=_aware(raw["starts_at"]),
            ends_at=_aware(raw["ends_at"]),
            timezone=raw["timezone"],
            venue=Venue(**raw["venue"]),
            dress_code=raw["dress_code"],
            rsvp_deadline=_aware(raw["rsvp_deadline"]),
            max_guests_per_rsvp=int(raw["max_guests_per_rsvp"]),
            programme=tuple(
                ProgrammeItem(starts_at=_aware(item["starts_at"]), title=item["title"])
                for item in raw["programme"]
            ),
        )


def _aware(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"Datetime '{value}' in the event file must include a UTC offset.")
    return parsed

import re
from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from app.domain.exceptions import InvalidRsvpError

NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 80
MESSAGE_MAX_LENGTH = 300
PHONE_PATTERN = re.compile(r"^\+?[\d\s()-]{7,20}$")


class Attendance(StrEnum):
    ATTENDING = "attending"
    DECLINED = "declined"


@dataclass(frozen=True, slots=True)
class RsvpDetails:
    """What a guest tells us. Validated and normalised on construction."""

    guest_name: str
    attendance: Attendance
    guest_count: int
    phone: str | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        name = " ".join(self.guest_name.split())
        phone = (self.phone or "").strip() or None
        message = (self.message or "").strip() or None

        if not NAME_MIN_LENGTH <= len(name) <= NAME_MAX_LENGTH:
            raise InvalidRsvpError(
                f"Name must be between {NAME_MIN_LENGTH} and {NAME_MAX_LENGTH} characters.",
                field="guest_name",
            )
        if phone is not None and not PHONE_PATTERN.fullmatch(phone):
            raise InvalidRsvpError("Please enter a valid phone number.", field="phone")
        if message is not None and len(message) > MESSAGE_MAX_LENGTH:
            raise InvalidRsvpError(
                f"Message must be at most {MESSAGE_MAX_LENGTH} characters.", field="message"
            )

        guest_count = self.guest_count
        if self.attendance is Attendance.DECLINED:
            guest_count = 0
        elif guest_count < 1:
            raise InvalidRsvpError("At least one guest must attend.", field="guest_count")

        object.__setattr__(self, "guest_name", name)
        object.__setattr__(self, "phone", phone)
        object.__setattr__(self, "message", message)
        object.__setattr__(self, "guest_count", guest_count)


@dataclass(frozen=True, slots=True)
class Rsvp:
    id: UUID
    details: RsvpDetails
    edit_token_hash: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, details: RsvpDetails, *, edit_token_hash: str, now: datetime) -> "Rsvp":
        return cls(
            id=uuid4(),
            details=details,
            edit_token_hash=edit_token_hash,
            created_at=now,
            updated_at=now,
        )

    def revise(self, details: RsvpDetails, *, now: datetime) -> "Rsvp":
        return replace(self, details=details, updated_at=now)

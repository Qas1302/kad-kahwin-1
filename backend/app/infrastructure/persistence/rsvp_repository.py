from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Attendance, Rsvp, RsvpDetails
from app.infrastructure.persistence.models import RsvpModel


class SqlAlchemyRsvpRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, rsvp: Rsvp) -> None:
        model = RsvpModel(id=str(rsvp.id))
        _copy_to_model(rsvp, model)
        self._session.add(model)
        self._session.commit()

    def update(self, rsvp: Rsvp) -> None:
        model = self._session.get(RsvpModel, str(rsvp.id))
        if model is None:
            raise LookupError(f"RSVP {rsvp.id} does not exist")
        _copy_to_model(rsvp, model)
        self._session.commit()

    def get(self, rsvp_id: UUID) -> Rsvp | None:
        model = self._session.get(RsvpModel, str(rsvp_id))
        return _to_entity(model) if model else None

    def list_all(self) -> list[Rsvp]:
        models = self._session.scalars(select(RsvpModel).order_by(RsvpModel.created_at))
        return [_to_entity(model) for model in models]


def _copy_to_model(rsvp: Rsvp, model: RsvpModel) -> None:
    details = rsvp.details
    model.guest_name = details.guest_name
    model.phone = details.phone
    model.attendance = details.attendance.value
    model.guest_count = details.guest_count
    model.message = details.message
    model.edit_token_hash = rsvp.edit_token_hash
    model.created_at = rsvp.created_at
    model.updated_at = rsvp.updated_at


def _to_entity(model: RsvpModel) -> Rsvp:
    return Rsvp(
        id=UUID(str(model.id)),
        details=RsvpDetails(
            guest_name=model.guest_name,
            attendance=Attendance(model.attendance),
            guest_count=model.guest_count,
            phone=model.phone,
            message=model.message,
        ),
        edit_token_hash=model.edit_token_hash,
        created_at=_as_utc(model.created_at),
        updated_at=_as_utc(model.updated_at),
    )


def _as_utc(value: datetime) -> datetime:
    # SQLite drops the offset; values are always written in UTC.
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.database import Base


class RsvpModel(Base):
    __tablename__ = "rsvps"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    guest_name: Mapped[str] = mapped_column(String(80))
    phone: Mapped[str | None] = mapped_column(String(20))
    attendance: Mapped[str] = mapped_column(String(16), index=True)
    guest_count: Mapped[int] = mapped_column(Integer)
    message: Mapped[str | None] = mapped_column(String(300))
    edit_token_hash: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

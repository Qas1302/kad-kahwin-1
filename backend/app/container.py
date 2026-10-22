"""Composition root: the only place that knows every layer and wires them together."""

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.application.use_cases import GetEventOverview, GetRsvp, ListRsvps, SubmitRsvp, UpdateRsvp
from app.infrastructure.clock import SystemClock
from app.infrastructure.config import Settings
from app.infrastructure.event_repository import JsonEventRepository
from app.infrastructure.persistence.database import Database
from app.infrastructure.persistence.rsvp_repository import SqlAlchemyRsvpRepository
from app.infrastructure.security import Sha256TokenService


@dataclass
class Container:
    settings: Settings
    database: Database = field(init=False)
    events: JsonEventRepository = field(init=False)
    tokens: Sha256TokenService = field(default_factory=Sha256TokenService)
    clock: SystemClock = field(default_factory=SystemClock)

    def __post_init__(self) -> None:
        self.database = Database(self.settings.database_url.get_secret_value())
        self.events = JsonEventRepository(self.settings.event_file)

    def startup(self) -> None:
        if self.settings.auto_create_schema:
            self.database.create_schema()
        self.events.get()  # fail fast if the event file is missing or invalid

    # Use case factories. Request-scoped pieces (the DB session) are passed in.
    def get_event_overview(self) -> GetEventOverview:
        return GetEventOverview(self.events, self.clock)

    def submit_rsvp(self, session: Session) -> SubmitRsvp:
        return SubmitRsvp(self.events, SqlAlchemyRsvpRepository(session), self.tokens, self.clock)

    def update_rsvp(self, session: Session) -> UpdateRsvp:
        return UpdateRsvp(self.events, SqlAlchemyRsvpRepository(session), self.tokens, self.clock)

    def get_rsvp(self, session: Session) -> GetRsvp:
        return GetRsvp(SqlAlchemyRsvpRepository(session), self.tokens)

    def list_rsvps(self, session: Session) -> ListRsvps:
        return ListRsvps(SqlAlchemyRsvpRepository(session))

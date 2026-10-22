from app.application.dto import EventOverview
from app.application.ports import Clock, EventRepository


class GetEventOverview:
    def __init__(self, events: EventRepository, clock: Clock) -> None:
        self._events = events
        self._clock = clock

    def execute(self) -> EventOverview:
        event = self._events.get()
        return EventOverview(event=event, rsvp_open=event.is_rsvp_open(self._clock.now()))

from app.application.dto import RsvpReport, RsvpSummary
from app.application.ports import RsvpRepository
from app.domain.entities import Attendance


class ListRsvps:
    def __init__(self, rsvps: RsvpRepository) -> None:
        self._rsvps = rsvps

    def execute(self) -> RsvpReport:
        rsvps = self._rsvps.list_all()
        attending = [r for r in rsvps if r.details.attendance is Attendance.ATTENDING]
        summary = RsvpSummary(
            total_responses=len(rsvps),
            attending_responses=len(attending),
            declined_responses=len(rsvps) - len(attending),
            total_guests=sum(r.details.guest_count for r in attending),
        )
        return RsvpReport(summary=summary, rsvps=rsvps)

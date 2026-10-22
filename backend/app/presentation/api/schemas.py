from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.application.dto import EventOverview, RsvpInput, RsvpReport, SubmittedRsvp
from app.domain.entities import Attendance, Rsvp
from app.domain.entities.rsvp import MESSAGE_MAX_LENGTH, NAME_MAX_LENGTH


class VenueSchema(BaseModel):
    name: str
    address: str
    map_url: str


class ProgrammeItemSchema(BaseModel):
    starts_at: datetime
    title: str


class EventResponse(BaseModel):
    partner_one: str
    partner_two: str
    host_line: str
    invitation_message: str
    starts_at: datetime
    ends_at: datetime
    timezone: str
    venue: VenueSchema
    dress_code: str
    rsvp_deadline: datetime
    rsvp_open: bool
    max_guests_per_rsvp: int
    programme: list[ProgrammeItemSchema]

    @classmethod
    def from_overview(cls, overview: EventOverview) -> "EventResponse":
        e = overview.event
        return cls(
            partner_one=e.partner_one,
            partner_two=e.partner_two,
            host_line=e.host_line,
            invitation_message=e.invitation_message,
            starts_at=e.starts_at,
            ends_at=e.ends_at,
            timezone=e.timezone,
            venue=VenueSchema(name=e.venue.name, address=e.venue.address, map_url=e.venue.map_url),
            dress_code=e.dress_code,
            rsvp_deadline=e.rsvp_deadline,
            rsvp_open=overview.rsvp_open,
            max_guests_per_rsvp=e.max_guests_per_rsvp,
            programme=[ProgrammeItemSchema(starts_at=p.starts_at, title=p.title) for p in e.programme],
        )


class RsvpRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guest_name: str = Field(max_length=NAME_MAX_LENGTH * 2)
    phone: str | None = Field(default=None, max_length=40)
    attendance: Attendance
    guest_count: int = Field(default=1, ge=0, le=50)
    message: str | None = Field(default=None, max_length=MESSAGE_MAX_LENGTH * 2)

    def to_input(self) -> RsvpInput:
        return RsvpInput(
            guest_name=self.guest_name,
            attendance=self.attendance,
            guest_count=self.guest_count,
            phone=self.phone,
            message=self.message,
        )


class RsvpResponse(BaseModel):
    id: UUID
    guest_name: str
    phone: str | None
    attendance: Attendance
    guest_count: int
    message: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, rsvp: Rsvp) -> "RsvpResponse":
        d = rsvp.details
        return cls(
            id=rsvp.id,
            guest_name=d.guest_name,
            phone=d.phone,
            attendance=d.attendance,
            guest_count=d.guest_count,
            message=d.message,
            created_at=rsvp.created_at,
            updated_at=rsvp.updated_at,
        )


class RsvpCreatedResponse(RsvpResponse):
    edit_token: str = Field(description="Keep this to view or change the RSVP later.")

    @classmethod
    def from_submitted(cls, submitted: SubmittedRsvp) -> "RsvpCreatedResponse":
        base = RsvpResponse.from_entity(submitted.rsvp)
        return cls(**base.model_dump(), edit_token=submitted.edit_token)


class RsvpSummarySchema(BaseModel):
    total_responses: int
    attending_responses: int
    declined_responses: int
    total_guests: int


class RsvpReportResponse(BaseModel):
    summary: RsvpSummarySchema
    rsvps: list[RsvpResponse]

    @classmethod
    def from_report(cls, report: RsvpReport) -> "RsvpReportResponse":
        s = report.summary
        return cls(
            summary=RsvpSummarySchema(
                total_responses=s.total_responses,
                attending_responses=s.attending_responses,
                declined_responses=s.declined_responses,
                total_guests=s.total_guests,
            ),
            rsvps=[RsvpResponse.from_entity(r) for r in report.rsvps],
        )


class ErrorBody(BaseModel):
    code: str
    message: str
    field: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody

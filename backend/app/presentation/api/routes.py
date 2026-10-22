from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.use_cases import GetEventOverview, GetRsvp, ListRsvps, SubmitRsvp, UpdateRsvp
from app.presentation.api import dependencies as deps
from app.presentation.api.schemas import (
    ErrorResponse,
    EventResponse,
    RsvpCreatedResponse,
    RsvpReportResponse,
    RsvpRequest,
    RsvpResponse,
)

ERRORS = {
    status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
    status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponse},
}

router = APIRouter(prefix="/api/v1")


@router.get("/event", response_model=EventResponse, tags=["event"])
def read_event(use_case: Annotated[GetEventOverview, Depends(deps.get_event_overview)]) -> EventResponse:
    return EventResponse.from_overview(use_case.execute())


@router.post(
    "/rsvps",
    response_model=RsvpCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERRORS,
    tags=["rsvp"],
)
def create_rsvp(
    body: RsvpRequest,
    use_case: Annotated[SubmitRsvp, Depends(deps.submit_rsvp)],
) -> RsvpCreatedResponse:
    return RsvpCreatedResponse.from_submitted(use_case.execute(body.to_input()))


@router.get("/rsvps/{rsvp_id}", response_model=RsvpResponse, responses=ERRORS, tags=["rsvp"])
def read_rsvp(
    rsvp_id: UUID,
    edit_token: deps.EditToken,
    use_case: Annotated[GetRsvp, Depends(deps.get_rsvp)],
) -> RsvpResponse:
    return RsvpResponse.from_entity(use_case.execute(rsvp_id, edit_token))


@router.put("/rsvps/{rsvp_id}", response_model=RsvpResponse, responses=ERRORS, tags=["rsvp"])
def replace_rsvp(
    rsvp_id: UUID,
    body: RsvpRequest,
    edit_token: deps.EditToken,
    use_case: Annotated[UpdateRsvp, Depends(deps.update_rsvp)],
) -> RsvpResponse:
    return RsvpResponse.from_entity(use_case.execute(rsvp_id, edit_token, body.to_input()))


@router.get(
    "/admin/rsvps",
    response_model=RsvpReportResponse,
    dependencies=[Depends(deps.require_admin)],
    tags=["admin"],
)
def read_rsvp_report(use_case: Annotated[ListRsvps, Depends(deps.list_rsvps)]) -> RsvpReportResponse:
    return RsvpReportResponse.from_report(use_case.execute())

import secrets
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.application.use_cases import GetEventOverview, GetRsvp, ListRsvps, SubmitRsvp, UpdateRsvp
from app.container import Container


def get_container(request: Request) -> Container:
    return request.app.state.container


ContainerDep = Annotated[Container, Depends(get_container)]


def get_session(container: ContainerDep) -> Iterator[Session]:
    yield from container.database.session()


SessionDep = Annotated[Session, Depends(get_session)]


def get_event_overview(container: ContainerDep) -> GetEventOverview:
    return container.get_event_overview()


def submit_rsvp(container: ContainerDep, session: SessionDep) -> SubmitRsvp:
    return container.submit_rsvp(session)


def update_rsvp(container: ContainerDep, session: SessionDep) -> UpdateRsvp:
    return container.update_rsvp(session)


def get_rsvp(container: ContainerDep, session: SessionDep) -> GetRsvp:
    return container.get_rsvp(session)


def list_rsvps(container: ContainerDep, session: SessionDep) -> ListRsvps:
    return container.list_rsvps(session)


def require_admin(
    container: ContainerDep,
    x_admin_key: Annotated[str | None, Header()] = None,
) -> None:
    configured = container.settings.admin_api_key
    if configured is None or not configured.get_secret_value():
        # Admin endpoints are off until a key is configured.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    if x_admin_key is None or not secrets.compare_digest(x_admin_key, configured.get_secret_value()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin key")


EditToken = Annotated[str, Header(alias="X-Rsvp-Token", min_length=1, max_length=128)]

class DomainError(Exception):
    """Base class for business rule violations."""

    code = "domain_error"

    def __init__(self, message: str, *, field: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.field = field


class InvalidRsvpError(DomainError):
    code = "invalid_rsvp"


class RsvpClosedError(DomainError):
    code = "rsvp_closed"


class RsvpNotFoundError(DomainError):
    code = "rsvp_not_found"


class RsvpAccessDeniedError(DomainError):
    code = "rsvp_access_denied"

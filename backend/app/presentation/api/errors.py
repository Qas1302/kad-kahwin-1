from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DomainError,
    InvalidRsvpError,
    RsvpAccessDeniedError,
    RsvpClosedError,
    RsvpNotFoundError,
)

STATUS_BY_ERROR: dict[type[DomainError], int] = {
    InvalidRsvpError: status.HTTP_422_UNPROCESSABLE_CONTENT,
    RsvpClosedError: status.HTTP_409_CONFLICT,
    RsvpNotFoundError: status.HTTP_404_NOT_FOUND,
    RsvpAccessDeniedError: status.HTTP_403_FORBIDDEN,
}


def _error(status_code: int, code: str, message: str, field: str | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "field": field}},
    )


async def _domain_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, DomainError)
    status_code = STATUS_BY_ERROR.get(type(exc), status.HTTP_400_BAD_REQUEST)
    return _error(status_code, exc.code, exc.message, exc.field)


async def _validation_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    first = exc.errors()[0] if exc.errors() else {}
    location = [str(part) for part in first.get("loc", ()) if part not in ("body", "header", "path")]
    return _error(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        "validation_error",
        first.get("msg", "Invalid request."),
        location[-1] if location else None,
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, _domain_error)
    app.add_exception_handler(RequestValidationError, _validation_error)

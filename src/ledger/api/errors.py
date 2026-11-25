from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ledger.domain.errors import AccountClosedError, AccountNotFoundError, LedgerError

_STATUS_BY_ERROR: dict[type[LedgerError], int] = {
    AccountNotFoundError: status.HTTP_404_NOT_FOUND,
    AccountClosedError: status.HTTP_409_CONFLICT,
}


async def _ledger_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """Render domain errors as RFC 7807 problem+json."""
    assert isinstance(exc, LedgerError)
    code = _STATUS_BY_ERROR.get(type(exc), status.HTTP_400_BAD_REQUEST)
    return JSONResponse(
        status_code=code,
        media_type="application/problem+json",
        content={
            "type": f"urn:ledger:error:{type(exc).__name__}",
            "title": type(exc).__name__,
            "status": code,
            "detail": str(exc),
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(LedgerError, _ledger_error_handler)

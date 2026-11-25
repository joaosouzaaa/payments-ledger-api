from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ledger.api.errors import register_error_handlers
from ledger.api.v1 import accounts_router
from ledger.db.session import dispose_engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await dispose_engine()


def create_app() -> FastAPI:
    app = FastAPI(title="Payments Ledger API", version="0.1.0", lifespan=lifespan)
    register_error_handlers(app)
    app.include_router(accounts_router.router, prefix="/api/v1")
    return app


app = create_app()

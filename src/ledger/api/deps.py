from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ledger.db.session import get_session
from ledger.repositories.accounts import AccountRepository
from ledger.services.accounts import AccountService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_account_service(session: SessionDep) -> AccountService:
    return AccountService(AccountRepository(session))


AccountServiceDep = Annotated[AccountService, Depends(get_account_service)]

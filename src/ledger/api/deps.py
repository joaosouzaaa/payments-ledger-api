from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ledger.db.session import get_session
from ledger.repositories.account_repository import AccountRepository
from ledger.services.account_service import AccountService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_account_service(session: SessionDep) -> AccountService:
    return AccountService(AccountRepository(session))


AccountServiceDep = Annotated[AccountService, Depends(get_account_service)]

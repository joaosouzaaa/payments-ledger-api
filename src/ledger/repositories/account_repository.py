from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ledger.common.pagination import PageList, PageParameters, paginate
from ledger.db.models import Account


class AccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, account: Account) -> Account:
        self._session.add(account)
        await self._session.flush()
        await self._session.refresh(account)
        return account

    async def commit(self) -> None:
        await self._session.commit()

    async def get(self, account_id: UUID) -> Account | None:
        return await self._session.get(Account, account_id)

    async def list(self, page_parameters: PageParameters) -> PageList[Account]:
        query = select(Account).order_by(Account.created_at, Account.id)
        return await paginate(self._session, query, page_parameters)

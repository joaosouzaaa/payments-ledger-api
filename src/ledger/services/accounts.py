from collections.abc import Sequence
from uuid import UUID

from ledger.db.models import Account
from ledger.domain.enums import AccountStatus, AccountType
from ledger.domain.errors import AccountClosedError, AccountNotFoundError
from ledger.repositories.accounts import AccountRepository


class AccountService:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    async def create(self, *, name: str, type: AccountType, currency: str) -> Account:
        account = await self._repository.add(Account(name=name, type=type, currency=currency))
        await self._repository.commit()
        return account

    async def get(self, account_id: UUID) -> Account:
        account = await self._repository.get(account_id)
        if account is None:
            raise AccountNotFoundError(account_id)
        return account

    async def list(self, *, limit: int, offset: int) -> Sequence[Account]:
        return await self._repository.list(limit=limit, offset=offset)

    async def rename(self, account_id: UUID, name: str) -> Account:
        account = await self.get(account_id)
        if account.status is AccountStatus.CLOSED:
            raise AccountClosedError(account_id)
        account.name = name
        await self._repository.commit()
        return account

    async def close(self, account_id: UUID) -> Account:
        # TODO(transactions): refuse to close an account with a non-zero balance.
        account = await self.get(account_id)
        account.status = AccountStatus.CLOSED
        await self._repository.commit()
        return account

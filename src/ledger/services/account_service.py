from uuid import UUID

from ledger.common.pagination import PageList, PageParameters
from ledger.db.models import Account
from ledger.domain.enums import AccountStatus
from ledger.domain.errors import AccountNotFoundError
from ledger.repositories.account_repository import AccountRepository


class AccountService:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    async def create(self, name: str) -> Account:
        account = await self._repository.add(Account(name=name))
        await self._repository.commit()
        return account

    async def get(self, account_id: UUID) -> Account:
        account = await self._repository.get(account_id)
        if account is None:
            raise AccountNotFoundError(account_id)
        return account

    async def list(self, page_parameters: PageParameters) -> PageList[Account]:
        return await self._repository.list(page_parameters)

    async def close(self, account_id: UUID) -> Account:
        # TODO(transactions): refuse to close an account with a non-zero balance.
        account = await self.get(account_id)
        account.status = AccountStatus.CLOSED
        await self._repository.commit()
        return account

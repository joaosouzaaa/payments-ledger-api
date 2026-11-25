from uuid import UUID

from ledger.domain.errors.ledger_error import LedgerError


class AccountNotFoundError(LedgerError):
    def __init__(self, account_id: UUID) -> None:
        super().__init__(f"Account {account_id} not found.")
        self.account_id = account_id

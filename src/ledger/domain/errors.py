from uuid import UUID


class LedgerError(Exception):
    """Base class for domain errors. The API layer maps these to HTTP problem responses."""


class AccountNotFoundError(LedgerError):
    def __init__(self, account_id: UUID) -> None:
        super().__init__(f"Account {account_id} not found.")
        self.account_id = account_id


class AccountClosedError(LedgerError):
    def __init__(self, account_id: UUID) -> None:
        super().__init__(f"Account {account_id} is closed.")
        self.account_id = account_id

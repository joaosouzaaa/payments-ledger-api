from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ledger.domain.enums import AccountStatus, AccountType

AccountName = Annotated[str, Field(min_length=1, max_length=100)]
CurrencyCode = Annotated[str, Field(pattern=r"^[A-Z]{3}$", description="ISO 4217 code, e.g. EUR")]


class AccountCreate(BaseModel):
    name: AccountName
    type: AccountType
    currency: CurrencyCode


class AccountUpdate(BaseModel):
    name: AccountName


class AccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    type: AccountType
    currency: str
    status: AccountStatus
    created_at: datetime

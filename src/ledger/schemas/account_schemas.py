from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ledger.domain.enums import AccountStatus

AccountName = Annotated[str, Field(min_length=1, max_length=100)]


class AccountCreate(BaseModel):
    name: AccountName


class AccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    status: AccountStatus
    created_at: datetime

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from ledger.api.deps import AccountServiceDep
from ledger.schemas.accounts import AccountCreate, AccountRead, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(body: AccountCreate, service: AccountServiceDep) -> AccountRead:
    account = await service.create(name=body.name, type=body.type, currency=body.currency)
    return AccountRead.model_validate(account)


@router.get("", response_model=list[AccountRead])
async def list_accounts(
    service: AccountServiceDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[AccountRead]:
    accounts = await service.list(limit=limit, offset=offset)
    return [AccountRead.model_validate(a) for a in accounts]


@router.get("/{account_id}", response_model=AccountRead)
async def get_account(account_id: UUID, service: AccountServiceDep) -> AccountRead:
    return AccountRead.model_validate(await service.get(account_id))


@router.patch("/{account_id}", response_model=AccountRead)
async def update_account(
    account_id: UUID, body: AccountUpdate, service: AccountServiceDep
) -> AccountRead:
    return AccountRead.model_validate(await service.rename(account_id, body.name))


@router.post("/{account_id}/close", response_model=AccountRead)
async def close_account(account_id: UUID, service: AccountServiceDep) -> AccountRead:
    return AccountRead.model_validate(await service.close(account_id))

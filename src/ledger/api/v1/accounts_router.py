from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from ledger.api.deps import AccountServiceDep
from ledger.common.pagination import PageList, PageParameters
from ledger.schemas.account_schemas import AccountCreate, AccountRead

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(body: AccountCreate, service: AccountServiceDep) -> AccountRead:
    return AccountRead.model_validate(await service.create(body.name))


@router.get("", response_model=PageList[AccountRead])
async def list_accounts(
    service: AccountServiceDep, page_parameters: Annotated[PageParameters, Query()]
) -> PageList[AccountRead]:
    page = await service.list(page_parameters)
    return page.map(AccountRead.model_validate)


@router.get("/{account_id}", response_model=AccountRead)
async def get_account(account_id: UUID, service: AccountServiceDep) -> AccountRead:
    return AccountRead.model_validate(await service.get(account_id))


@router.post("/{account_id}/close", response_model=AccountRead)
async def close_account(account_id: UUID, service: AccountServiceDep) -> AccountRead:
    return AccountRead.model_validate(await service.close(account_id))

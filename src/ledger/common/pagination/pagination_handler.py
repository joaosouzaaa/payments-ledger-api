from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ledger.common.pagination.page_list import PageList
from ledger.common.pagination.page_parameters import PageParameters


async def paginate[T](
    session: AsyncSession, query: Select[T], page_parameters: PageParameters
) -> PageList[T]:
    """Runs a count query plus the requested page. The query must have a deterministic ORDER BY."""
    total_count = await session.scalar(
        select(func.count()).select_from(query.order_by(None).subquery())
    )
    items = await session.scalars(
        query.offset(page_parameters.offset).limit(page_parameters.page_size)
    )
    return PageList.create(items.all(), total_count or 0, page_parameters)

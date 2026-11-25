import math
from collections.abc import Callable, Sequence

from pydantic import BaseModel, ConfigDict

from ledger.common.pagination.page_parameters import PageParameters


class PageList[T](BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_page: int
    total_pages: int
    page_size: int
    total_count: int
    result: list[T]

    @classmethod
    def create(
        cls, items: Sequence[T], total_count: int, page_parameters: PageParameters
    ) -> PageList[T]:
        return cls(
            current_page=page_parameters.page_number,
            total_pages=math.ceil(total_count / page_parameters.page_size),
            page_size=page_parameters.page_size,
            total_count=total_count,
            result=list(items),
        )

    def map[U](self, mapper: Callable[[T], U]) -> PageList[U]:
        return PageList[U](
            current_page=self.current_page,
            total_pages=self.total_pages,
            page_size=self.page_size,
            total_count=self.total_count,
            result=[mapper(item) for item in self.result],
        )

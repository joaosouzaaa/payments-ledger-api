from typing import Annotated

from pydantic import BaseModel, Field

MAX_PAGE_SIZE = 100


class PageParameters(BaseModel):
    """Query parameters for paged endpoints. Invalid values are rejected with a 422."""

    page_number: Annotated[int, Field(ge=1)] = 1
    page_size: Annotated[int, Field(ge=1, le=MAX_PAGE_SIZE)] = 10

    @property
    def offset(self) -> int:
        return (self.page_number - 1) * self.page_size

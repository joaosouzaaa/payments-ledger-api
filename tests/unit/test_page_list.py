import pytest
from pydantic import ValidationError

from ledger.common.pagination import PageList, PageParameters


@pytest.mark.parametrize(
    ("total_count", "page_size", "expected_pages"),
    [(0, 10, 0), (1, 10, 1), (10, 10, 1), (11, 10, 2), (25, 10, 3)],
)
def test_total_pages_rounds_up(total_count: int, page_size: int, expected_pages: int) -> None:
    page = PageList[int].create([], total_count, PageParameters(page_number=1, page_size=page_size))

    assert page.total_pages == expected_pages
    assert page.total_count == total_count


def test_create_copies_page_parameters() -> None:
    page = PageList[str].create(["a", "b"], 5, PageParameters(page_number=3, page_size=2))

    assert (page.current_page, page.page_size, page.result) == (3, 2, ["a", "b"])


def test_map_transforms_items_and_keeps_metadata() -> None:
    page = PageList[int].create([1, 2], 7, PageParameters(page_number=2, page_size=2))

    mapped = page.map(str)

    assert mapped.result == ["1", "2"]
    assert (mapped.current_page, mapped.total_pages, mapped.total_count) == (2, 4, 7)


@pytest.mark.parametrize("kwargs", [{"page_number": 0}, {"page_size": 0}, {"page_size": 101}])
def test_page_parameters_reject_invalid_values(kwargs: dict[str, int]) -> None:
    with pytest.raises(ValidationError):
        PageParameters(**kwargs)


def test_offset_skips_previous_pages() -> None:
    assert PageParameters(page_number=3, page_size=20).offset == 40

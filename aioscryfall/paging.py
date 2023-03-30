import asyncio
import contextlib
from typing import TYPE_CHECKING, AsyncIterable, TypeVar, cast

from . import responses
from .models import List, RawList

if TYPE_CHECKING:
    from aiohttp import ClientSession


T = TypeVar("T")


async def depage_list(session: "ClientSession", paged_list: List[T]) -> AsyncIterable[T]:
    """Iterate over a paged list, calling next page as needed."""
    current_page: List[T] | None = paged_list
    while current_page is not None:
        next_page_task = None
        if current_page.next_page is not None:
            next_page_task = asyncio.create_task(session.get(current_page.next_page))

        for item in current_page.data:
            yield item

        current_page = None
        if next_page_task is not None:
            with contextlib.closing(await next_page_task) as next_page_resp:
                current_page = cast(List[T], await responses.parse(next_page_resp, RawList))

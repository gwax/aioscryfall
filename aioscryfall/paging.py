"""Paging utilities for Scryfall list responses."""

import asyncio
import contextlib
from collections.abc import AsyncIterable
from typing import TYPE_CHECKING, TypeVar

from aioscryfall.api import responses
from aioscryfall.models.lists import ScryList, ScryListable

if TYPE_CHECKING:
    from aiohttp import ClientSession


_T = TypeVar("_T", bound=ScryListable)


async def depage_list(session: "ClientSession", paged_list: ScryList[_T]) -> AsyncIterable[_T]:
    """Iterate over a paged list, calling next page as needed."""
    current_page: ScryList[_T] | None = paged_list
    while current_page is not None:
        next_page_task = None
        if current_page.next_page is not None:
            next_page_task = asyncio.create_task(session.get(current_page.next_page))

        for item in current_page.data:
            yield item

        current_page = None
        if next_page_task is not None:
            with contextlib.closing(await next_page_task) as next_page_resp:
                current_page = await responses.read_response_payload(next_page_resp, ScryList[_T])

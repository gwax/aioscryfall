import asyncio
import contextlib
from typing import TYPE_CHECKING, AsyncIterable

import msgspec

from .models import List

if TYPE_CHECKING:
    from aiohttp import ClientSession

    from .models import Listable


async def depage_list(
    session: "ClientSession", paged_list: List
) -> AsyncIterable["Listable"]:
    """Iterate over a paged list, calling next page as needed."""
    list_decoder: msgspec.json.Decoder | None = None
    current_page: List | None = paged_list
    while current_page is not None:
        next_page_task = None
        if current_page.next_page is not None:
            next_page_task = asyncio.create_task(session.get(current_page.next_page))

        for item in current_page.data:
            yield item

        current_page = None
        if next_page_task is not None:
            with contextlib.closing(await next_page_task) as next_page_resp:
                if list_decoder is None:
                    list_decoder = msgspec.json.Decoder(List)
                current_page = list_decoder.decode(await next_page_resp.read())

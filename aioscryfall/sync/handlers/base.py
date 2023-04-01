"""Base class for all synchronous handlers."""

import asyncio
from collections.abc import AsyncIterable, Awaitable, Iterable
from typing import Callable, TypeVar

import aiohttp

from aioscryfall.client import ScryfallClient

_T = TypeVar("_T")


class BaseSyncHandler:
    """Base class for all synchronous handlers."""

    def _result_extract(self, extractor: Callable[[ScryfallClient], Awaitable[_T]]) -> _T:
        """Convert an asynchronous call to ScryfallClient into a synchronous result."""

        async def inner() -> _T:
            """Inner function to be called by the event loop."""
            async with aiohttp.ClientSession() as session:
                async_client = ScryfallClient(session)
                return await extractor(async_client)

        return asyncio.run(inner())

    def _iterable_extract(
        self, extractor: Callable[[ScryfallClient], AsyncIterable[_T]]
    ) -> Iterable[_T]:
        """Convert an asynchronous call to ScryfallClient into a synchronous iterable."""

        async def inner() -> AsyncIterable[_T]:
            """Inner function to be called by the event loop."""
            async with aiohttp.ClientSession() as session:
                async_client = ScryfallClient(session)
                async for item in extractor(async_client):
                    yield item

        loop = asyncio.get_event_loop()
        async_iterator = aiter(inner())
        while True:
            try:
                yield loop.run_until_complete(anext(async_iterator))
            except StopAsyncIteration:
                break

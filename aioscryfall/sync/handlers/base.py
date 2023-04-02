"""Base class for all synchronous handlers."""

import asyncio
import functools
from collections.abc import AsyncIterable, Awaitable, Coroutine, Iterable
from typing import TYPE_CHECKING, Callable, Concatenate, ParamSpec, TypeVar

import aiohttp

from aioscryfall.client import ScryfallClient

if TYPE_CHECKING:
    from aioscryfall.sync.client import ScryfallSyncClient

_T = TypeVar("_T")


class BaseSyncHandler:
    """Base class for all synchronous handlers."""

    def __init__(self, client: "ScryfallSyncClient") -> None:
        self._client = client

    def _result_extract(self, extractor: Callable[[ScryfallClient], Awaitable[_T]]) -> _T:
        """Convert an asynchronous call to ScryfallClient into a synchronous result."""

        async def inner() -> _T:
            """Inner function to be called by the event loop."""
            return await extractor(self._client.get_async_client())

        loop = self._client.get_event_loop()
        return loop.run_until_complete(inner())

    def _iterable_extract(
        self, extractor: Callable[[ScryfallClient], AsyncIterable[_T]]
    ) -> Iterable[_T]:
        """Convert an asynchronous call to ScryfallClient into a synchronous iterable."""

        async def inner() -> AsyncIterable[_T]:
            """Inner function to be called by the event loop."""
            async for item in extractor(self._client.get_async_client()):
                yield item

        loop = self._client.get_event_loop()
        async_iterator = aiter(inner())
        while True:
            try:
                yield loop.run_until_complete(anext(async_iterator))
            except StopAsyncIteration:
                break

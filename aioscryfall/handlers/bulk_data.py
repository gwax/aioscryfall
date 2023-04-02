"""Client handler for the Scryfall bulk data APIs."""

import gc
import gzip
import os
from collections.abc import AsyncIterable, Awaitable
from contextvars import ContextVar
from typing import overload
from uuid import UUID

import appdirs
from requests_cache import CachedSession, SerializerPipeline, Stage, pickle_serializer

from aioscryfall.api import bulk_data
from aioscryfall.models import serde
from aioscryfall.models.bulk_data import ScryBulkData
from aioscryfall.models.lists import ScryListable

from .base import BaseHandler

_CACHED_REQUESTS_SESSION: ContextVar[CachedSession | None] = ContextVar(
    "_CACHED_REQUESTS_SESSION", default=None
)


def _get_requests_session() -> CachedSession:
    cache = _CACHED_REQUESTS_SESSION.get()
    if cache is None:
        cache_dir = appdirs.user_cache_dir("aioscryfall")
        cache_file = os.path.join(cache_dir, "requests_cache.sqlite")
        serializer = SerializerPipeline(
            [
                pickle_serializer,
                Stage(dumps=gzip.compress, loads=gzip.decompress),
            ],
            is_binary=True,
        )
        cache = CachedSession(
            cache_file,
            backend="sqlite",
            serializer=serializer,
            cache_control=True,
            expire_after=86400,
        )
        _CACHED_REQUESTS_SESSION.set(cache)
    return cache


class BulkDataHandler(BaseHandler):
    """ScryfallClient handler for bulk_data APIs."""

    async def all_bulk_data(self) -> AsyncIterable[ScryBulkData]:
        """Get all bulk data."""
        async with self._client.limiter:
            first_page = await bulk_data.all_bulk_data(self._client.session)
        async for bulk_data_item in self._client.depage_list(first_page):
            yield bulk_data_item

    @overload
    def get_bulk_data(self, *, bulk_data_id: UUID) -> Awaitable[ScryBulkData]:
        ...

    @overload
    def get_bulk_data(self, *, bulk_data_type: str) -> Awaitable[ScryBulkData]:
        ...

    async def get_bulk_data(
        self,
        *,
        bulk_data_id: UUID | None = None,
        bulk_data_type: str | None = None,
    ) -> ScryBulkData:
        """Get a single bulk data item."""
        has_identifier = (
            bulk_data_id is not None,
            bulk_data_type is not None,
        )
        invalid_args_msg = "Exactly one of bulk_data_id, bulk_data_type must be specified."
        if len([x for x in has_identifier if x]) != 1:
            raise ValueError(invalid_args_msg)
        async with self._client.limiter:
            if bulk_data_id is not None:
                return await bulk_data.getby_id(self._client.session, bulk_data_id)
            if bulk_data_type is not None:
                return await bulk_data.getby_type(self._client.session, bulk_data_type)
            raise ValueError(invalid_args_msg)

    async def fetch_contents(self, bulk_data_item: ScryBulkData) -> list[ScryListable]:
        """Fetch the contents of a bulk data item."""
        # TODO: This should be async but aiohttp-client-cache doesn't support the use of
        #       etag + If-None-Match to handle Cache-Control and I do not want to implement
        #       that myself.
        session = _get_requests_session()
        async with self._client.limiter:
            response = session.get(bulk_data_item.download_uri)
        response.raise_for_status()
        try:
            gc.disable()
            item_list = serde.decode_json(response.content, list[ScryListable])
        finally:
            gc.enable()
        return item_list

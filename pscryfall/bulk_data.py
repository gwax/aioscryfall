"""Scryfall API client implementation for Bulk Data Objects.

Documentation: https://scryfall.com/docs/api/bulk-data
"""

import gzip
import os
from contextvars import ContextVar
from typing import TYPE_CHECKING

import appdirs
import msgspec
from requests_cache import CachedSession, SerializerPipeline, Stage, pickle_serializer

from . import responses
from .models import BulkData, List, Listable

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientSession

BULK_FILE_CACHE: ContextVar[CachedSession | None] = ContextVar(
    "BULK_FILE_CACHE", default=None
)


def _get_requests_session() -> CachedSession:
    cache = BULK_FILE_CACHE.get()
    if cache is None:
        cache_dir = appdirs.user_cache_dir("pscryfall")
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
        BULK_FILE_CACHE.set(cache)
    return cache


async def all_bulk_data(session: "ClientSession") -> List[BulkData]:
    """Client implementation for the Scryfall API's /bulk-data endpoint.

    Documentation: https://scryfall.com/docs/api/bulk-data/all
    """
    url = "https://api.scryfall.com/bulk-data"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[BulkData])


async def get(session: "ClientSession", scryfall_id: "UUID") -> BulkData:
    """Client implementation for the Scryfall API's /bulk-data/:id endpoint.

    Documentation: https://scryfall.com/docs/api/bulk-data/id
    """
    url = f"https://api.scryfall.com/bulk-data/{scryfall_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, BulkData)


async def bulk_data_type(session: "ClientSession", bulk_data_type: str) -> BulkData:
    """Client implementation for the Scryfall API's /bulk-data/:type endpoint.

    Documentation: https://scryfall.com/docs/api/bulk-data/type
    """
    url = f"https://api.scryfall.com/bulk-data/{bulk_data_type}"
    async with session.get(url) as resp:
        return await responses.parse(resp, BulkData)


async def fetch(bulk_data: BulkData) -> list[Listable]:
    """Fetch and parse a given bulk data file.

    Documentation: https://scryfall.com/docs/api/bulk-data/files
    """
    # TODO: This should be async but aiohttp-client-cache doesn't support the use of
    #       etag + If-None-Match to handle Cache-Control and I do not want to implement
    #       that myself.
    session = _get_requests_session()
    response = session.get(bulk_data.download_uri)
    response.raise_for_status()
    return msgspec.json.decode(response.content, type=list[Listable])

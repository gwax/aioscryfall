"""Scryfall API client implementation for Bulk Data Objects.

Documentation: https://scryfall.com/docs/api/bulk-data
"""

from typing import TYPE_CHECKING

from aioscryfall.models.bulk_data import ScryBulkData
from aioscryfall.models.lists import ScryList

from . import responses

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientSession


async def all_bulk_data(session: "ClientSession") -> ScryList[ScryBulkData]:
    """Client implementation for the Scryfall API's /bulk-data endpoint.

    Documentation: https://scryfall.com/docs/api/bulk-data/all
    """
    url = "https://api.scryfall.com/bulk-data"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryBulkData])


async def getby_id(session: "ClientSession", scryfall_id: "UUID") -> ScryBulkData:
    """Client implementation for the Scryfall API's /bulk-data/:id endpoint.

    Documentation: https://scryfall.com/docs/api/bulk-data/id
    """
    url = f"https://api.scryfall.com/bulk-data/{scryfall_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryBulkData)


async def getby_type(session: "ClientSession", type_: str) -> ScryBulkData:
    """Client implementation for the Scryfall API's /bulk-data/:type endpoint.

    Documentation: https://scryfall.com/docs/api/bulk-data/type
    """
    url = f"https://api.scryfall.com/bulk-data/{type_}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryBulkData)

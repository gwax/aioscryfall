"""Scryfall API client implementation for Set Objects.

Documentation: https://scryfall.com/docs/api/sets
"""

from typing import TYPE_CHECKING

from aioscryfall.models.lists import ScryList
from aioscryfall.models.sets import ScrySet

from . import responses

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientSession


async def all_sets(session: "ClientSession") -> ScryList[ScrySet]:
    """Client implementation for the Scryfall API's /sets endpoint.

    Documentation: https://scryfall.com/docs/api/sets/all
    """
    url = "https://api.scryfall.com/sets"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScrySet])


async def getby_code(session: "ClientSession", set_code: str) -> ScrySet:
    """Client implementation for the Scryfall API's /sets/:code endpoint.

    Documentation: https://scryfall.com/docs/api/sets/code
    """
    url = f"https://api.scryfall.com/sets/{set_code}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScrySet)


async def getby_tcgplayer_id(session: "ClientSession", tcgplayer_id: int) -> ScrySet:
    """Client implementation for the Scryfall API's /sets/tcgplayer/:id endpoint.

    Documentation: https://scryfall.com/docs/api/sets/tcgplayer
    """
    url = f"https://api.scryfall.com/sets/tcgplayer/{tcgplayer_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScrySet)


async def getby_id(session: "ClientSession", scryfall_id: "UUID") -> ScrySet:
    """Client implementation for the Scryfall API's /sets/:id endpoint.

    Documentation: https://scryfall.com/docs/api/sets/id
    """
    url = f"https://api.scryfall.com/sets/{scryfall_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScrySet)

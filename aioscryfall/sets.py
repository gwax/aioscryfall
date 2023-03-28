"""Scryfall API client implementation for Set Objects.

Documentation: https://scryfall.com/docs/api/sets
"""

from typing import TYPE_CHECKING

from . import responses
from .models import List, Set

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientSession


async def all_sets(session: "ClientSession") -> List[Set]:
    """Client implementation for the Scryfall API's /sets endpoint.

    Documentation: https://scryfall.com/docs/api/sets/all
    """
    url = "https://api.scryfall.com/sets"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[Set])


async def code(session: "ClientSession", set_code: str) -> Set:
    """Client implementation for the Scryfall API's /sets/:code endpoint.

    Documentation: https://scryfall.com/docs/api/sets/code
    """
    url = f"https://api.scryfall.com/sets/{set_code}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Set)


async def tcgplayer_id(session: "ClientSession", tcgplayer_id: int) -> Set:
    """Client implementation for the Scryfall API's /sets/tcgplayer/:id endpoint.

    Documentation: https://scryfall.com/docs/api/sets/tcgplayer
    """
    url = f"https://api.scryfall.com/sets/tcgplayer/{tcgplayer_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Set)


async def get(session: "ClientSession", scryfall_id: "UUID") -> Set:
    """Client implementation for the Scryfall API's /sets/:id endpoint.

    Documentation: https://scryfall.com/docs/api/sets/id
    """
    url = f"https://api.scryfall.com/sets/{scryfall_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Set)

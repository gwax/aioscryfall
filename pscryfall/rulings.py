"""Scryfall API client implementation for Ruling Objects.

Documentation: https://scryfall.com/docs/api/rulings
"""

from typing import TYPE_CHECKING

from . import responses
from .models import List, Ruling

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientSession


async def card(session: "ClientSession", scryfall_id: "UUID") -> List[Ruling]:
    """Client implementation for the Scryfall API's /cards/:id/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/card
    """
    url = f"https://api.scryfall.com/cards/{scryfall_id}/rulings"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[Ruling])


async def multiverse_id(session: "ClientSession", multiverse_id: int) -> List[Ruling]:
    """Client implementation for the Scryfall API's /cards/multiverse/:id/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/multiverse
    """
    url = f"https://api.scryfall.com/cards/multiverse/{multiverse_id}/rulings"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[Ruling])


async def mtgo_id(session: "ClientSession", mtgo_id: int) -> List[Ruling]:
    """Client implementation for the Scryfall API's /cards/mtgo/:id/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/mtgo
    """
    url = f"https://api.scryfall.com/cards/mtgo/{mtgo_id}/rulings"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[Ruling])


async def arena_id(session: "ClientSession", arena_id: int) -> List[Ruling]:
    """Client implementation for the Scryfall API's /cards/arena/:id/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/arena
    """
    url = f"https://api.scryfall.com/cards/arena/{arena_id}/rulings"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[Ruling])


async def set_code_and_number(
    session: "ClientSession", set_code: str, collector_number: str
) -> List[Ruling]:
    """Client implementation for the Scryfall API's /cards/:set/:number/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/set
    """
    url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}/rulings"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[Ruling])

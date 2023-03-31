"""Scryfall API client implementation for Ruling Objects.

Documentation: https://scryfall.com/docs/api/rulings
"""

from typing import TYPE_CHECKING

from aioscryfall.models.lists import ScryList
from aioscryfall.models.rulings import ScryRuling

from . import responses

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientSession


async def getby_card_id(session: "ClientSession", scryfall_id: "UUID") -> ScryList[ScryRuling]:
    """Client implementation for the Scryfall API's /cards/:id/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/card
    """
    url = f"https://api.scryfall.com/cards/{scryfall_id}/rulings"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryRuling])


async def getby_multiverse_id(
    session: "ClientSession", multiverse_id: int
) -> ScryList[ScryRuling]:
    """Client implementation for the Scryfall API's /cards/multiverse/:id/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/multiverse
    """
    url = f"https://api.scryfall.com/cards/multiverse/{multiverse_id}/rulings"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryRuling])


async def getby_mtgo_id(session: "ClientSession", mtgo_id: int) -> ScryList[ScryRuling]:
    """Client implementation for the Scryfall API's /cards/mtgo/:id/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/mtgo
    """
    url = f"https://api.scryfall.com/cards/mtgo/{mtgo_id}/rulings"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryRuling])


async def getby_arena_id(session: "ClientSession", arena_id: int) -> ScryList[ScryRuling]:
    """Client implementation for the Scryfall API's /cards/arena/:id/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/arena
    """
    url = f"https://api.scryfall.com/cards/arena/{arena_id}/rulings"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryRuling])


async def getby_set_code_and_number(
    session: "ClientSession", set_code: str, collector_number: str
) -> ScryList[ScryRuling]:
    """Client implementation for the Scryfall API's /cards/:set/:number/rulings endpoint.

    Documentation: https://scryfall.com/docs/api/rulings/set
    """
    url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}/rulings"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryRuling])

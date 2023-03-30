"""Scryfall API client implementation for Symbol Objects and Mana Cost Objects.

Documentation: https://scryfall.com/docs/api/card-symbols
"""

from typing import TYPE_CHECKING

from aioscryfall.models.lists import ScryList
from aioscryfall.models.symbols import ScryCardSymbol, ScryManaCost

from . import responses

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def all_card_symbols(session: "ClientSession") -> ScryList[ScryCardSymbol]:
    """Client implementation for the Scryfall API's /symbology endpoint.

    Documentation: https://scryfall.com/docs/api/card-symbols/all
    """
    url = "https://api.scryfall.com/symbology"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryCardSymbol])


async def parse_mana(session: "ClientSession", mana_cost: str) -> ScryManaCost:
    """Client implementation for the Scryfall API's /symbology/parse-mana endpoint.

    Documentation: https://scryfall.com/docs/api/card-symbols/parse-mana
    """
    url = f"https://api.scryfall.com/symbology/parse-mana?cost={mana_cost}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryManaCost)

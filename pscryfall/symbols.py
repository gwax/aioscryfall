"""Scryfall API client implementation for Symbol Objects and Mana Cost Objects.

Documentation: https://scryfall.com/docs/api/card-symbols
"""

from typing import TYPE_CHECKING

from . import responses
from .models import CardSymbol, List, ManaCost

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def all_card_symbols(session: "ClientSession") -> List[CardSymbol]:
    """Client implementation for the Scryfall API's /symbology endpoint.

    Documentation: https://scryfall.com/docs/api/card-symbols/all
    """
    url = "https://api.scryfall.com/symbology"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[CardSymbol])


async def parse_mana(session: "ClientSession", mana_cost: str) -> ManaCost:
    """Client implementation for the Scryfall API's /symbology/parse-mana endpoint.

    Documentation: https://scryfall.com/docs/api/card-symbols/parse-mana
    """
    url = f"https://api.scryfall.com/symbology/parse-mana?cost={mana_cost}"
    async with session.get(url) as resp:
        return await responses.parse(resp, ManaCost)

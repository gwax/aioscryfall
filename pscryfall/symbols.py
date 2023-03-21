"""Scryfall API client implementation for Symbol Objects and Mana Cost Objects.

Documentation: https://scryfall.com/docs/api/card-symbols
"""

from typing import TYPE_CHECKING

import msgspec

from .models import List

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def all_card_symbols(session: "ClientSession") -> List:
    """Client implementation for the Scryfall API's /symbology endpoint.

    Documentation: https://scryfall.com/docs/api/card-symbols/all
    """
    url = "https://api.scryfall.com/symbology"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=List)


async def parse_mana(session: "ClientSession", mana_cost: str) -> List:
    """Client implementation for the Scryfall API's /symbology/parse-mana endpoint.

    Documentation: https://scryfall.com/docs/api/card-symbols/parse-mana
    """
    url = f"https://api.scryfall.com/symbology/parse?cost={mana_cost}"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=List)

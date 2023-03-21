"""Scryfall API client implementation for Catalog Objects.

Documentation: https://scryfall.com/docs/api/catalogs
"""

from typing import TYPE_CHECKING

import msgspec

from .models import Catalog

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def card_names(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/card-names endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/card-names
    """
    url = "https://api.scryfall.com/catalog/card-names"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def artist_names(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/artist-names endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/artist-names
    """
    url = "https://api.scryfall.com/catalog/artist-names"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def word_bank(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/word-bank endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/word-bank
    """
    url = "https://api.scryfall.com/catalog/word-bank"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def creature_types(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/creature-types endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/creature-types
    """
    url = "https://api.scryfall.com/catalog/creature-types"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def planeswalker_types(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/planeswalker-types endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/planeswalker-types
    """
    url = "https://api.scryfall.com/catalog/planeswalker-types"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def land_types(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/land-types endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/land-types
    """
    url = "https://api.scryfall.com/catalog/land-types"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def artifact_types(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/artifact-types endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/artifact-types
    """
    url = "https://api.scryfall.com/catalog/artifact-types"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def enchantment_types(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/enchantment-types endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/enchantment-types
    """
    url = "https://api.scryfall.com/catalog/enchantment-types"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def spell_types(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/spell-types endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/spell-types
    """
    url = "https://api.scryfall.com/catalog/spell-types"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def powers(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/powers endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/powers
    """
    url = "https://api.scryfall.com/catalog/powers"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def toughnesses(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/toughnesses endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/toughnesses
    """
    url = "https://api.scryfall.com/catalog/toughnesses"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def loyalties(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/loyalties endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/loyalties
    """
    url = "https://api.scryfall.com/catalog/loyalties"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def watermarks(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/watermarks endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/watermarks
    """
    url = "https://api.scryfall.com/catalog/watermarks"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def keyword_abilities(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/keyword-abilities endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/keyword-abilities
    """
    url = "https://api.scryfall.com/catalog/keyword-abilities"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def keyword_actions(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/keyword-actions endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/keyword-actions
    """
    url = "https://api.scryfall.com/catalog/keyword-actions"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)


async def ability_words(session: "ClientSession") -> Catalog:
    """Client implementation for the Scryfall API's /catalog/ability-words endpoint.

    Documentation: https://scryfall.com/docs/api/catalogs/ability-words
    """
    url = "https://api.scryfall.com/catalog/ability-words"
    async with session.get(url) as resp:
        return msgspec.json.decode(await resp.read(), type=Catalog)

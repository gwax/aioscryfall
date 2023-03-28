"""Scryfall API client implementation for Card Migrations.

Documentation: https://scryfall.com/docs/api/migrations
"""

from typing import TYPE_CHECKING

from . import responses
from .models import List, Migration

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientSession


async def all_migrations(session: "ClientSession") -> List[Migration]:
    """Client implementation for the Scryfall API's /migrations endpoint.

    Documentation: https://scryfall.com/docs/api/migrations/all
    """
    url = "https://api.scryfall.com/migrations"
    async with session.get(url) as resp:
        return await responses.parse(resp, List[Migration])


async def get(session: "ClientSession", scryfall_id: "UUID") -> Migration:
    """Client implementation for the Scryfall API's /migrations/:id endpoint.

    Documentation: https://scryfall.com/docs/api/migrations/id
    """
    url = f"https://api.scryfall.com/migrations/{scryfall_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Migration)

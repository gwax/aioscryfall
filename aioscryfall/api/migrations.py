"""Scryfall API client implementation for Card Migrations.

Documentation: https://scryfall.com/docs/api/migrations
"""

from typing import TYPE_CHECKING

from aioscryfall.models.lists import ScryList
from aioscryfall.models.migrations import ScryMigration

from . import responses

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientSession


async def all_migrations(session: "ClientSession") -> ScryList[ScryMigration]:
    """Client implementation for the Scryfall API's /migrations endpoint.

    Documentation: https://scryfall.com/docs/api/migrations/all
    """
    url = "https://api.scryfall.com/migrations"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryMigration])


async def getby_id(session: "ClientSession", scryfall_id: "UUID") -> ScryMigration:
    """Client implementation for the Scryfall API's /migrations/:id endpoint.

    Documentation: https://scryfall.com/docs/api/migrations/id
    """
    url = f"https://api.scryfall.com/migrations/{scryfall_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryMigration)

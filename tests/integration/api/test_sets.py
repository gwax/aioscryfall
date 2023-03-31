"""Integration tests for aioscryfall.api.sets."""

from typing import TYPE_CHECKING
from uuid import UUID

from aioscryfall.api import sets

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def test_all_sets(client_session: "ClientSession") -> None:
    result = await sets.all_sets(client_session)
    assert result.data


async def test_code(client_session: "ClientSession") -> None:
    result = await sets.getby_code(client_session, "ice")
    assert result.code == "ice"
    assert result.name == "Ice Age"


async def test_tcgplayer_id(client_session: "ClientSession") -> None:
    result = await sets.getby_tcgplayer_id(client_session, 1857)
    assert result.code == "aer"
    assert result.name == "Aether Revolt"


async def test_get(client_session: "ClientSession") -> None:
    result = await sets.getby_id(client_session, UUID("a4a0db50-8826-4e73-833c-3fd934375f96"))
    assert result.code == "aer"
    assert result.name == "Aether Revolt"

"""Tests for aioscryfall.api.migrations."""

from typing import TYPE_CHECKING
from uuid import UUID

from aioscryfall.api import migrations
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_all_migrations(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test all_migrations."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/migrations", "migrations/page1.json"
    )
    result = await migrations.all_migrations(client_session)
    assert UUID("ebb0bc4b-6e01-40ae-a9c8-af08b144141b") in {m.old_scryfall_id for m in result.data}


async def test_getby_id(mock_aioresponse: "aioresponses", client_session: "ClientSession") -> None:
    """Test getby_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/migrations/a7d78fca-990e-471d-b965-7a757bc38250",
        "migrations/single.json",
    )
    result = await migrations.getby_id(
        client_session, UUID("a7d78fca-990e-471d-b965-7a757bc38250")
    )
    assert result.old_scryfall_id == UUID("ebb0bc4b-6e01-40ae-a9c8-af08b144141b")

"""Tests for aioscryfall.api.bulk_data."""

from typing import TYPE_CHECKING
from uuid import UUID

from aioscryfall.api import bulk_data
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_all_bulk_data(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test all_bulk_data."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/bulk-data", "bulk_data/all.json"
    )
    result = await bulk_data.all_bulk_data(client_session)
    assert "Oracle Cards" in {bd.name for bd in result.data}


async def test_getby_id(mock_aioresponse: "aioresponses", client_session: "ClientSession") -> None:
    """Test getby_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/bulk-data/00000000-0000-0000-0000-000000000003",
        "bulk_data/single.json",
    )
    result = await bulk_data.getby_id(client_session, UUID(int=3))
    assert result.name == "Oracle Cards"


async def test_getby_type(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_type."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/bulk-data/oracle-cards",
        "bulk_data/single.json",
    )
    result = await bulk_data.getby_type(client_session, "oracle-cards")
    assert result.name == "Oracle Cards"

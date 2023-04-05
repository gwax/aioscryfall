"""Tests for aioscryfall.api.sets."""

from typing import TYPE_CHECKING
from uuid import UUID

from aioscryfall.api import sets
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_all_sets(mock_aioresponse: "aioresponses", client_session: "ClientSession") -> None:
    """Test all_sets."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/sets", "sets/page1.json"
    )
    result = await sets.all_sets(client_session)
    assert "mom" in {s.code for s in result.data}
    assert result.next_page == "https://api.scryfall.com/sets?page=2"


async def test_getby_code(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_code."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/sets/isd", "sets/single.json"
    )
    result = await sets.getby_code(client_session, "isd")
    assert result.code


async def test_getby_tcgplayer_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_tcgplayer_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/sets/tcgplayer/123",
        "sets/single.json",
    )
    result = await sets.getby_tcgplayer_id(client_session, 123)
    assert result.code


async def test_getby_id(mock_aioresponse: "aioresponses", client_session: "ClientSession") -> None:
    """Test getby_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/sets/00000000-0000-0000-0000-000000000001",
        "sets/single.json",
    )
    result = await sets.getby_id(client_session, UUID(int=1))
    assert result.code

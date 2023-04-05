"""Tests for aioscryfall.api.rulings."""

from typing import TYPE_CHECKING
from uuid import UUID

from aioscryfall.api import rulings
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_getby_card_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_card_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/00000000-0000-0000-0000-000000000001/rulings",
        "rulings/single-card.json",
    )
    result = await rulings.getby_card_id(client_session, UUID(int=1))
    assert len(result.data) == 2


async def test_getby_multiverse_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_multiverse_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/multiverse/123/rulings",
        "rulings/single-card.json",
    )
    result = await rulings.getby_multiverse_id(client_session, 123)
    assert len(result.data) == 2


async def test_getby_mtgo_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_mtgo_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/mtgo/123/rulings",
        "rulings/single-card.json",
    )
    result = await rulings.getby_mtgo_id(client_session, 123)
    assert len(result.data) == 2


async def test_getby_arena_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_arena_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/arena/123/rulings",
        "rulings/single-card.json",
    )
    result = await rulings.getby_arena_id(client_session, 123)
    assert len(result.data) == 2


async def test_getby_set_code_and_collector_number(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_set_code_and_collector_number."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/rtr/213/rulings",
        "rulings/single-card.json",
    )
    result = await rulings.getby_set_code_and_collector_number(client_session, "rtr", "213")
    assert len(result.data) == 2

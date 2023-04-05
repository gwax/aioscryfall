"""Tests for aioscryfall.api.symbols."""

from typing import TYPE_CHECKING

from aioscryfall.api import symbols
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_all_card_symbols(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test all_card_symbols."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/symbology", "symbols/card-symbols-page1.json"
    )
    result = await symbols.all_card_symbols(client_session)
    assert result.data
    assert "{T}" in {symbol.symbol for symbol in result.data}


async def test_parse_mana(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test parse_mana."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/symbology/parse-mana?cost=BGUX",
        "symbols/parse-mana-single.json",
    )
    result = await symbols.parse_mana(client_session, "BGUX")
    assert result.cost == "{X}{B}{G}{U}"

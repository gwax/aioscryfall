"""Integration tests for aioscryfall.api.symbols."""

from typing import TYPE_CHECKING

import pytest

from aioscryfall.api import symbols
from aioscryfall.errors import APIError
from aioscryfall.models.common import ScryColor

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def test_all_card_symbols(client_session: "ClientSession") -> None:
    result = await symbols.all_card_symbols(client_session)
    assert result.data
    [tap_symbol] = [s for s in result.data if s.symbol == "{T}"]
    assert tap_symbol.english == "tap this permanent"


async def test_parse_mana(client_session: "ClientSession") -> None:
    result = await symbols.parse_mana(client_session, "1GU")
    assert result.cost == "{1}{G}{U}"
    assert result.colors == [ScryColor.BLUE, ScryColor.GREEN]
    assert result.cmc == 3


async def test_parse_mana_error(client_session: "ClientSession") -> None:
    with pytest.raises(APIError) as err:
        await symbols.parse_mana(client_session, "stuff")
    assert err.value.status >= 400
    assert err.value.status == err.value.error.status
    assert err.value.error.code == "validation_error"

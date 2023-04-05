"""Tests for aioscryfall.api.responses errors."""

from typing import TYPE_CHECKING

import pytest

from aioscryfall.api import symbols
from aioscryfall.errors import APIError, UnparsedAPIError
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_parseable_error(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test parseable_error."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/symbology/parse-mana?cost=invalid",
        "errors/parse-mana.json",
        status_code=422,
    )
    with pytest.raises(APIError) as err:
        await symbols.parse_mana(client_session, "invalid")
    assert err.value.status == 422
    assert err.value.error.status == 422
    assert err.value.error.code == "validation_error"


async def test_unparseable_error(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test unparseable error."""
    mock_aioresponse.get(
        "https://api.scryfall.com/symbology/parse-mana?cost=embiggen",
        status=500,
        body=b"perfectly cromulent word",
    )
    with pytest.raises(UnparsedAPIError) as err:
        await symbols.parse_mana(client_session, "embiggen")
    assert err.value.status == 500
    assert err.value.details == b"perfectly cromulent word"

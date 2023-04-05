"""Tests for aioscryfall.client."""

from typing import TYPE_CHECKING

from aioscryfall import client
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_cards_search(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test search."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/cards/search?q=foo", "cards/forests-page1.json"
    )
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/search?some_args=stuff",
        "cards/forests-page2.json",
    )

    scryfall_client = client.ScryfallClient(client_session)
    result = [card async for card in scryfall_client.cards.search("foo")]
    assert len(result) == 20

    mock_aioresponse.assert_any_call("https://api.scryfall.com/cards/search?q=foo")
    mock_aioresponse.assert_any_call("https://api.scryfall.com/cards/search?some_args=stuff")

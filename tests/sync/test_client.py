"""Tests for aioscryfall.sync.client."""

from typing import TYPE_CHECKING

from aioscryfall.sync import client
from tests import utils

if TYPE_CHECKING:
    from aioresponses import aioresponses


def test_cards_search(mock_aioresponse: "aioresponses") -> None:
    """Test search."""
    utils.sync_load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/cards/search?q=foo", "cards/forests-page1.json"
    )
    utils.sync_load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/search?some_args=stuff",
        "cards/forests-page2.json",
    )

    scryfall_client = client.ScryfallSyncClient()
    result = list(scryfall_client.cards.search("foo"))
    assert len(result) == 20

    mock_aioresponse.assert_any_call("https://api.scryfall.com/cards/search?q=foo")
    mock_aioresponse.assert_any_call("https://api.scryfall.com/cards/search?some_args=stuff")

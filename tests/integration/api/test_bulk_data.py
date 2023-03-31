"""Integration tests for aioscryfall.api.bulk_data."""

from typing import TYPE_CHECKING

from aioscryfall.api import bulk_data
from aioscryfall.models.rulings import ScryRuling

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def test_bulk_data_endpoints(client_session: "ClientSession") -> None:
    result = await bulk_data.all_bulk_data(client_session)
    assert result.data
    [default_cards_bulk] = [d for d in result.data if d.type_ == "default_cards"]
    assert default_cards_bulk.download_uri
    assert default_cards_bulk.name == "Default Cards"

    scryfall_id = default_cards_bulk.id_
    default_cards_bulk2 = await bulk_data.getby_id(client_session, scryfall_id)
    assert default_cards_bulk2 == default_cards_bulk

    default_cards_bulk3 = await bulk_data.getby_type(client_session, "default_cards")
    assert default_cards_bulk3 == default_cards_bulk


async def test_fetch(client_session: "ClientSession") -> None:
    rulings_bulk = await bulk_data.getby_type(client_session, "rulings")
    assert rulings_bulk.download_uri

    rulings = await bulk_data.fetch(rulings_bulk)
    assert rulings
    assert isinstance(rulings[0], ScryRuling)

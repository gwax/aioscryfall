"""Tests for aioscryfall.api.cards."""

from typing import TYPE_CHECKING
from uuid import UUID

from aioscryfall.api import cards
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_search__no_options(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test search."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/cards/search?q=foo", "cards/forests-page1.json"
    )
    result = await cards.search(client_session, "foo")
    assert result.total_cards == 20
    assert result.data[0].name == "Arctic Treeline"
    assert result.has_more
    assert result.next_page == "https://api.scryfall.com/cards/search?some_args=stuff"


async def test_search__all_options(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test search."""
    await utils.load_get_payload(
        mock_aioresponse,
        (
            "https://api.scryfall.com/cards/search"
            "?dir=asc"
            "&include_extras=true"
            "&include_multilingual=true"
            "&include_variations=true"
            "&order=name"
            "&page=2"
            "&q=foo"
            "&unique=prints"
        ),
        "cards/forests-page2.json",
    )
    result = await cards.search(
        client_session,
        "foo",
        unique=cards.UniqueMode.PRINTS,
        order=cards.SortOrdering.NAME,
        direction=cards.SortDirection.ASC,
        include_extras=True,
        include_multilingual=True,
        include_variations=True,
        page=2,
    )
    assert result.data[0].name == "Bayou"
    assert not result.has_more
    assert result.next_page is None


async def test_named__exact(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test named."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/cards/named?exact=foo", "cards/single.json"
    )
    result = await cards.named(client_session, exact="foo")
    assert result.name == "Urza's Saga"


async def test_named__exact_with_set_code(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test named."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/named?exact=foo&set=isd",
        "cards/single.json",
    )
    result = await cards.named(client_session, exact="foo", set_code="isd")
    assert result.name == "Urza's Saga"


async def test_named__fuzzy(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test named."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/cards/named?fuzzy=foo", "cards/single.json"
    )
    result = await cards.named(client_session, fuzzy="foo")
    assert result.name == "Urza's Saga"


async def test_named__fuzzy_with_set_code(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test named."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/named?fuzzy=foo&set=isd",
        "cards/single.json",
    )
    result = await cards.named(client_session, fuzzy="foo", set_code="isd")
    assert result.name == "Urza's Saga"


async def test_autocomplete(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test autocomplete."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/autocomplete?q=snow",
        "cards/autocomplete.json",
    )
    result = await cards.autocomplete(client_session, "snow")
    assert result.total_values == 5
    assert "Snow-Covered Island" in result.data


async def test_autocomplete__with_include_extras(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test autocomplete."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/autocomplete?q=snow&include_extras=true",
        "cards/autocomplete.json",
    )
    result = await cards.autocomplete(client_session, "snow", include_extras=True)
    assert result.total_values == 5
    assert "Snow-Covered Island" in result.data


async def test_random(mock_aioresponse: "aioresponses", client_session: "ClientSession") -> None:
    """Test random."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/cards/random", "cards/single.json"
    )
    result = await cards.random(client_session)
    assert result.name == "Urza's Saga"


async def test_collection(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test collection."""
    await utils.load_post_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/collection",
        "cards/forests-page1.json",
    )
    result = await cards.collection(client_session, [{"name": "foo"}])
    assert result.total_cards == 20
    assert result.data[0].name == "Arctic Treeline"
    assert result.has_more
    assert result.next_page == "https://api.scryfall.com/cards/search?some_args=stuff"

    mock_aioresponse.assert_called_once_with(
        "https://api.scryfall.com/cards/collection",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=b'{"identifiers":[{"name":"foo"}]}',
    )


async def test_getby_set_code_and_collector_number(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_set_code_and_collector_number."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/isd/1",
        "cards/single.json",
    )
    result = await cards.getby_set_code_and_collector_number(client_session, "isd", 1)
    assert result.name == "Urza's Saga"


async def test_getby_set_code_and_collector_number__with_language(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_set_code_and_collector_number."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/isd/1/fr",
        "cards/single.json",
    )
    result = await cards.getby_set_code_and_collector_number(client_session, "isd", 1, lang="fr")
    assert result.name == "Urza's Saga"


async def test_getby_multiverse_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_multiverse_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/multiverse/1",
        "cards/single.json",
    )
    result = await cards.getby_multiverse_id(client_session, 1)
    assert result.name == "Urza's Saga"


async def test_getby_mtgo_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_mtgo_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/mtgo/1",
        "cards/single.json",
    )
    result = await cards.getby_mtgo_id(client_session, 1)
    assert result.name == "Urza's Saga"


async def test_getby_arenta_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_arenta_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/arena/1",
        "cards/single.json",
    )
    result = await cards.getby_arena_id(client_session, 1)
    assert result.name == "Urza's Saga"


async def test_getby_tcgplayer_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_tcgplayer_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/tcgplayer/1",
        "cards/single.json",
    )
    result = await cards.getby_tcgplayer_id(client_session, 1)
    assert result.name == "Urza's Saga"


async def test_getby_cardmarket_id(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test getby_cardmarket_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/cardmarket/1",
        "cards/single.json",
    )
    result = await cards.getby_cardmarket_id(client_session, 1)
    assert result.name == "Urza's Saga"


async def test_getby_id(mock_aioresponse: "aioresponses", client_session: "ClientSession") -> None:
    """Test getby_id."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/cards/00000000-0000-0000-0000-000000000003",
        "cards/single.json",
    )
    result = await cards.getby_id(client_session, UUID(int=3))
    assert result.name == "Urza's Saga"

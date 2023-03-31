"""Integration tests for aioscryfall.api.cards."""

from typing import TYPE_CHECKING
from uuid import UUID

import pytest

from aioscryfall.api import cards
from aioscryfall.api.cards import CardIdentifier, SortDirection, SortOrdering, UniqueMode
from aioscryfall.errors import APIError
from aioscryfall.models.cards import ScryCard, ScryCardLayout

if TYPE_CHECKING:
    from aiohttp import ClientSession


class TestSearch:
    async def test_single_result(self, client_session: "ClientSession") -> None:
        result = await cards.search(client_session, "alexandria (game:paper)")
        [card] = result.data
        assert card.name == "Library of Alexandria"
        assert card.set_.upper() == "ARN"

    @pytest.mark.parametrize(
        ("query", "mode", "expected_count"),
        [
            ('!"Thallid" (game:paper)', None, 1),
            ('!"Thallid" (game:paper)', UniqueMode.CARDS, 1),
            ('!"Thallid" (game:paper)', UniqueMode.ART, 5),
            ('!"Thallid" (game:paper)', UniqueMode.PRINTS, 6),
        ],
    )
    async def test_unique_mode(
        self,
        client_session: "ClientSession",
        query: str,
        mode: UniqueMode | None,
        expected_count: int,
    ) -> None:
        result = await cards.search(client_session, query, unique=mode)
        assert len(result.data) == expected_count

    @pytest.mark.parametrize(
        ("query", "ordering", "direction", "expected_sets_and_numbers"),
        [
            (
                "orcish lumberjack (game:paper)",
                SortOrdering.RELEASED,
                SortDirection.ASC,
                [("ice", "210"), ("cst", "210"), ("ddl", "44"), ("plist", "480")],
            ),
            (
                "dark s:3ed",
                None,
                None,
                [("3ed", "100"), ("3ed", "99")],  # Darkpact, Dark Ritual
            ),
            (
                "dark s:3ed",
                SortOrdering.NAME,
                SortDirection.ASC,
                [("3ed", "100"), ("3ed", "99")],  # Darkpact, Dark Ritual
            ),
            (
                "dark s:3ed",
                SortOrdering.NAME,
                SortDirection.DESC,
                [("3ed", "99"), ("3ed", "100")],  # Dark Ritual, Darkpact
            ),
        ],
    )
    async def test_order_direction(
        self,
        client_session: "ClientSession",
        query: str,
        ordering: SortOrdering | None,
        direction: SortDirection | None,
        expected_sets_and_numbers: list[tuple[str, str]],
    ) -> None:
        result = await cards.search(
            client_session,
            query,
            unique=UniqueMode.PRINTS,
            order=ordering,
            direction=direction,
        )
        sets_and_numbers = [(card.set_, card.collector_number) for card in result.data]
        assert sets_and_numbers == expected_sets_and_numbers

    async def test_include_extras(self, client_session: "ClientSession") -> None:
        result_none = await cards.search(
            client_session, "tazeem (game:paper)", include_extras=None
        )
        assert {card.name for card in result_none.data} == {
            "Guardian of Tazeem",
            "Tazeem Raptor",
            "Tazeem Roilmage",
        }

        result_false = await cards.search(
            client_session, "tazeem (game:paper)", include_extras=False
        )
        assert {card.name for card in result_false.data} == {
            "Guardian of Tazeem",
            "Tazeem Raptor",
            "Tazeem Roilmage",
        }

        result_true = await cards.search(
            client_session, "tazeem (game:paper)", include_extras=True
        )
        assert {card.name for card in result_true.data} == {
            "Guardian of Tazeem",
            "Tazeem Raptor",
            "Tazeem Roilmage",
            "Tazeem Roilmage // Tazeem Roilmage",
            "Tazeem",
        }
        assert all(
            card.layout == ScryCardLayout.PLANAR
            for card in result_true.data
            if card.name == "Tazeem"
        )
        assert all(
            card.layout == ScryCardLayout.ART_SERIES
            for card in result_true.data
            if card.name == "Tazeem Roilmage // Tazeem Roilmage"
        )

    # TODO: test include_multilingual
    # TODO: test include_variations

    async def test_page(self, client_session: "ClientSession") -> None:
        result_page_none = await cards.search(
            client_session, '!"Forest"', unique=UniqueMode.PRINTS
        )
        assert len(result_page_none.data) == 175
        assert result_page_none.has_more
        assert result_page_none.next_page is not None
        assert isinstance(result_page_none.total_cards, int)
        assert result_page_none.total_cards > 700

        result_page_three = await cards.search(
            client_session, '!"Forest"', unique=UniqueMode.PRINTS, page=3
        )
        assert len(result_page_three.data) == 175
        assert result_page_three.has_more
        assert result_page_three.next_page is not None


class TestNamed:
    async def test_exact_success(self, client_session: "ClientSession") -> None:
        card = await cards.named(client_session, exact="library of alexandria")
        assert card.name == "Library of Alexandria"

        card2 = await cards.named(client_session, exact="orcish lumberjack", set_code="ice")
        assert card2.name == "Orcish Lumberjack"
        assert card2.set_ == "ice"

    async def test_exact_failure(self, client_session: "ClientSession") -> None:
        with pytest.raises(APIError) as err:
            await cards.named(client_session, exact="library of alexandria", set_code="ice")
        assert err.value.status == err.value.error.status == 404
        assert err.value.error.details is not None
        assert err.value.error.details.startswith("No cards found matching")

    async def test_fuzzy_success(self, client_session: "ClientSession") -> None:
        card = await cards.named(client_session, fuzzy="jace bleren")
        assert card.name == "Jace Beleren"

        card = await cards.named(client_session, fuzzy="jace", set_code="wwk")
        assert card.name == "Jace, the Mind Sculptor"
        assert card.set_ == "wwk"

    async def test_fuzzy_failure(self, client_session: "ClientSession") -> None:
        with pytest.raises(APIError) as err:
            await cards.named(client_session, fuzzy="jace")
        assert err.value.status == err.value.error.status == 404
        assert err.value.error.details is not None
        assert err.value.error.details.startswith("Too many cards match")


async def test_autocomplete(client_session: "ClientSession") -> None:
    result = await cards.autocomplete(client_session, "urza's s")
    assert set(result.data) == {
        "Urza's Saga",
        "Urza's Science Fair Project",
        "Urza's Sylex",
    }


async def test_random(client_session: "ClientSession") -> None:
    result = await cards.random(client_session)
    assert isinstance(result, ScryCard)


@pytest.mark.parametrize(
    ("identifiers", "expected_ids"),
    [
        (
            [
                {"id": "683a5707-cddb-494d-9b41-51b4584ded69"},
                {"name": "Ancient Tomb"},
                {"set": "mrd", "collector_number": "150"},
            ],
            [
                UUID("683a5707-cddb-494d-9b41-51b4584ded69"),
                UUID("bd3d4b4b-cf31-4f89-8140-9650edb03c7b"),
                UUID("1a02ca71-5e39-4a5f-aaba-a1e3e10a6a3e"),
            ],
        ),
        (
            [
                {"id": UUID("03bdcf52-50b8-42c0-9665-931d83f5f314")},
            ],
            [
                UUID("03bdcf52-50b8-42c0-9665-931d83f5f314"),
            ],
        ),
    ],
)
async def test_collection(
    client_session: "ClientSession",
    identifiers: list[CardIdentifier],
    expected_ids: list[UUID],
) -> None:
    result = await cards.collection(client_session, identifiers)
    assert [card.id_ for card in result.data] == expected_ids


async def test_set_code_and_number(
    client_session: "ClientSession",
) -> None:
    result = await cards.getby_set_code_and_number(client_session, "mrd", "150")
    assert result.name == "Chalice of the Void"


async def test_multiverse_id(client_session: "ClientSession") -> None:
    result = await cards.getby_multiverse_id(client_session, 48326)
    assert result.name == "Chalice of the Void"


async def test_mtgo_id(client_session: "ClientSession") -> None:
    result = await cards.getby_mtgo_id(client_session, 19995)
    assert result.name == "Chalice of the Void"


async def test_arena_id(client_session: "ClientSession") -> None:
    result = await cards.getby_arena_id(client_session, 67330)
    assert result.name == "Yargle, Glutton of Urborg"


async def test_tcgplayer_id(client_session: "ClientSession") -> None:
    result = await cards.getby_tcgplayer_id(client_session, 162145)
    assert result.name == "Rona, Disciple of Gix"


async def test_cardmarket_id(client_session: "ClientSession") -> None:
    result = await cards.getby_cardmarket_id(client_session, 379041)
    assert result.name == "Embodiment of Agonies"


async def test_get(client_session: "ClientSession") -> None:
    result = await cards.getby_id(client_session, UUID("f295b713-1d6a-43fd-910d-fb35414bf58a"))
    assert result.name == "Dusk // Dawn"

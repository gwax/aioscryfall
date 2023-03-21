"""Integration tests for pscryfall.catalogs."""

from typing import TYPE_CHECKING

from pscryfall import catalogs

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def test_card_names(session: "ClientSession") -> None:
    result = await catalogs.card_names(session)
    assert result.uri
    assert result.total_values > 0
    assert "Colossal Dreadmaw" in result.data


async def test_artist_names(session: "ClientSession") -> None:
    result = await catalogs.artist_names(session)
    assert result.uri
    assert result.total_values > 0
    assert "Mark Zug" in result.data


async def test_word_bank(session: "ClientSession") -> None:
    result = await catalogs.word_bank(session)
    assert result.uri
    assert result.total_values > 0
    assert "destroy" in result.data


async def test_creature_types(session: "ClientSession") -> None:
    result = await catalogs.creature_types(session)
    assert result.uri
    assert result.total_values > 0
    assert "Brushwagg" in result.data


async def test_planeswalker_types(session: "ClientSession") -> None:
    result = await catalogs.planeswalker_types(session)
    assert result.uri
    assert result.total_values > 0
    assert "Szat" in result.data


async def test_land_types(session: "ClientSession") -> None:
    result = await catalogs.land_types(session)
    assert result.uri
    assert result.total_values > 0
    assert "Locus" in result.data


async def test_artifact_types(session: "ClientSession") -> None:
    result = await catalogs.artifact_types(session)
    assert result.uri
    assert result.total_values > 0
    assert "Fortification" in result.data


async def test_enchantment_types(session: "ClientSession") -> None:
    result = await catalogs.enchantment_types(session)
    assert result.uri
    assert result.total_values > 0
    assert "Cartouche" in result.data


async def test_spell_types(session: "ClientSession") -> None:
    result = await catalogs.spell_types(session)
    assert result.uri
    assert result.total_values > 0
    assert "Arcane" in result.data


async def test_powers(session: "ClientSession") -> None:
    result = await catalogs.powers(session)
    assert result.uri
    assert result.total_values > 0
    assert "6" in result.data


async def test_toughnesses(session: "ClientSession") -> None:
    result = await catalogs.toughnesses(session)
    assert result.uri
    assert result.total_values > 0
    assert "6" in result.data


async def test_loyalties(session: "ClientSession") -> None:
    result = await catalogs.loyalties(session)
    assert result.uri
    assert result.total_values > 0
    assert "7" in result.data


async def test_watermarks(session: "ClientSession") -> None:
    result = await catalogs.watermarks(session)
    assert result.uri
    assert result.total_values > 0
    assert "phyrexian" in result.data


async def test_keyword_abilities(session: "ClientSession") -> None:
    result = await catalogs.keyword_abilities(session)
    assert result.uri
    assert result.total_values > 0
    assert "Phasing" in result.data


async def test_keyword_actions(session: "ClientSession") -> None:
    result = await catalogs.keyword_actions(session)
    assert result.uri
    assert result.total_values > 0
    assert "Regenerate" in result.data


async def test_ability_words(session: "ClientSession") -> None:
    result = await catalogs.ability_words(session)
    assert result.uri
    assert result.total_values > 0
    assert "Metalcraft" in result.data

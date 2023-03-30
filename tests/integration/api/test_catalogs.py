"""Integration tests for aioscryfall.api.catalogs."""

from typing import TYPE_CHECKING

from aioscryfall.api import catalogs

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def test_card_names(client_session: "ClientSession") -> None:
    result = await catalogs.card_names(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Colossal Dreadmaw" in result.data


async def test_artist_names(client_session: "ClientSession") -> None:
    result = await catalogs.artist_names(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Mark Zug" in result.data


async def test_word_bank(client_session: "ClientSession") -> None:
    result = await catalogs.word_bank(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "destroy" in result.data


async def test_creature_types(client_session: "ClientSession") -> None:
    result = await catalogs.creature_types(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Brushwagg" in result.data


async def test_planeswalker_types(client_session: "ClientSession") -> None:
    result = await catalogs.planeswalker_types(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Szat" in result.data


async def test_land_types(client_session: "ClientSession") -> None:
    result = await catalogs.land_types(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Locus" in result.data


async def test_artifact_types(client_session: "ClientSession") -> None:
    result = await catalogs.artifact_types(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Fortification" in result.data


async def test_enchantment_types(client_session: "ClientSession") -> None:
    result = await catalogs.enchantment_types(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Cartouche" in result.data


async def test_spell_types(client_session: "ClientSession") -> None:
    result = await catalogs.spell_types(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Arcane" in result.data


async def test_powers(client_session: "ClientSession") -> None:
    result = await catalogs.powers(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "6" in result.data


async def test_toughnesses(client_session: "ClientSession") -> None:
    result = await catalogs.toughnesses(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "6" in result.data


async def test_loyalties(client_session: "ClientSession") -> None:
    result = await catalogs.loyalties(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "7" in result.data


async def test_watermarks(client_session: "ClientSession") -> None:
    result = await catalogs.watermarks(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "phyrexian" in result.data


async def test_keyword_abilities(client_session: "ClientSession") -> None:
    result = await catalogs.keyword_abilities(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Phasing" in result.data


async def test_keyword_actions(client_session: "ClientSession") -> None:
    result = await catalogs.keyword_actions(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Regenerate" in result.data


async def test_ability_words(client_session: "ClientSession") -> None:
    result = await catalogs.ability_words(client_session)
    assert result.uri
    assert result.total_values > 0
    assert "Metalcraft" in result.data

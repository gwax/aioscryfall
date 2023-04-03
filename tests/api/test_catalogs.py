"""Tests for aioscryfall.api.catalogs."""

from typing import TYPE_CHECKING

from aioscryfall.api import catalogs
from tests import utils

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aioresponses import aioresponses


async def test_card_names(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test card_names."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/catalog/card-names", "catalog/card-names.json"
    )
    result = await catalogs.card_names(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/card-names"
    assert result.total_values
    assert "Colossal Dreadmaw" in result.data


async def test_artist_names(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test artist_names."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/artist-names",
        "catalog/artist-names.json",
    )
    result = await catalogs.artist_names(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/artist-names"
    assert result.total_values
    assert "Mark Zug" in result.data


async def test_word_bank(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test word_bank."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/catalog/word-bank", "catalog/word-bank.json"
    )
    result = await catalogs.word_bank(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/word-bank"
    assert result.total_values
    assert "destroy" in result.data


async def test_creature_types(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test creature_types."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/creature-types",
        "catalog/creature-types.json",
    )
    result = await catalogs.creature_types(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/creature-types"
    assert result.total_values
    assert "Brushwagg" in result.data


async def test_planeswalker_types(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test planeswalker_types."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/planeswalker-types",
        "catalog/planeswalker-types.json",
    )
    result = await catalogs.planeswalker_types(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/planeswalker-types"
    assert result.total_values
    assert "Szat" in result.data


async def test_land_types(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test land_types."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/catalog/land-types", "catalog/land-types.json"
    )
    result = await catalogs.land_types(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/land-types"
    assert result.total_values
    assert "Forest" in result.data


async def test_artifact_types(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test artifact_types."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/artifact-types",
        "catalog/artifact-types.json",
    )
    result = await catalogs.artifact_types(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/artifact-types"
    assert result.total_values
    assert "Equipment" in result.data


async def test_enchantment_types(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test enchantment_types."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/enchantment-types",
        "catalog/enchantment-types.json",
    )
    result = await catalogs.enchantment_types(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/enchantment-types"
    assert result.total_values
    assert "Cartouche" in result.data


async def test_spell_types(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test spell_types."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/spell-types",
        "catalog/spell-types.json",
    )
    result = await catalogs.spell_types(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/spell-types"
    assert result.total_values
    assert "Arcane" in result.data


async def test_powers(mock_aioresponse: "aioresponses", client_session: "ClientSession") -> None:
    """Test powers."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/catalog/powers", "catalog/powers.json"
    )
    result = await catalogs.powers(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/powers"
    assert result.total_values
    assert "2" in result.data


async def test_toughnesses(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test toughnesses."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/toughnesses",
        "catalog/toughnesses.json",
    )
    result = await catalogs.toughnesses(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/toughnesses"
    assert result.total_values
    assert "2" in result.data


async def test_loyalties(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test loyalties."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/catalog/loyalties", "catalog/loyalties.json"
    )
    result = await catalogs.loyalties(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/loyalties"
    assert result.total_values
    assert "2" in result.data


async def test_watermarks(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test watermarks."""
    await utils.load_get_payload(
        mock_aioresponse, "https://api.scryfall.com/catalog/watermarks", "catalog/watermarks.json"
    )
    result = await catalogs.watermarks(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/watermarks"
    assert result.total_values
    assert "fnm" in result.data


async def test_keyword_abilities(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test keyword_abilities."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/keyword-abilities",
        "catalog/keyword-abilities.json",
    )
    result = await catalogs.keyword_abilities(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/keyword-abilities"
    assert result.total_values
    assert "Living weapon" in result.data


async def test_keyword_actions(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test keyword_actions."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/keyword-actions",
        "catalog/keyword-actions.json",
    )
    result = await catalogs.keyword_actions(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/keyword-actions"
    assert result.total_values
    assert "Venture into the dungeon" in result.data


async def test_ability_words(
    mock_aioresponse: "aioresponses", client_session: "ClientSession"
) -> None:
    """Test ability_words."""
    await utils.load_get_payload(
        mock_aioresponse,
        "https://api.scryfall.com/catalog/ability-words",
        "catalog/ability-words.json",
    )
    result = await catalogs.ability_words(client_session)
    assert result.uri == "https://api.scryfall.com/catalog/ability-words"
    assert result.total_values
    assert "Metalcraft" in result.data

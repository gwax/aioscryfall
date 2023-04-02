"""Synchronous client handler for Scryfall catalogs APIs."""

from typing import TYPE_CHECKING

from .base import BaseSyncHandler

if TYPE_CHECKING:
    from aioscryfall.client import ScryfallClient


class CatalogsSyncHandler(BaseSyncHandler):
    """ScryfallSyncClient handler for catalogs APIs."""

    def card_names(self) -> list[str]:
        """Get a list of all card names."""
        return self._result_extract(lambda c: c.catalogs.card_names())

    def artist_names(self) -> list[str]:
        """Get a list of all artist names."""
        return self._result_extract(lambda c: c.catalogs.artist_names())

    def word_bank(self) -> list[str]:
        """Get a list of all words used in card text."""
        return self._result_extract(lambda c: c.catalogs.word_bank())

    def creature_types(self) -> list[str]:
        """Get a list of all creature types."""
        return self._result_extract(lambda c: c.catalogs.creature_types())

    def planeswalker_types(self) -> list[str]:
        """Get a list of all planeswalker types."""
        return self._result_extract(lambda c: c.catalogs.planeswalker_types())

    def land_types(self) -> list[str]:
        """Get a list of all land types."""
        return self._result_extract(lambda c: c.catalogs.land_types())

    def artifact_types(self) -> list[str]:
        """Get a list of all artifact types."""
        return self._result_extract(lambda c: c.catalogs.artifact_types())

    def enchantment_types(self) -> list[str]:
        """Get a list of all enchantment types."""
        return self._result_extract(lambda c: c.catalogs.enchantment_types())

    def spell_types(self) -> list[str]:
        """Get a list of all spell types."""
        return self._result_extract(lambda c: c.catalogs.spell_types())

    def powers(self) -> list[str]:
        """Get a list of all powers."""
        return self._result_extract(lambda c: c.catalogs.powers())

    def toughnesses(self) -> list[str]:
        """Get a list of all toughnesses."""
        return self._result_extract(lambda c: c.catalogs.toughnesses())

    def loyalties(self) -> list[str]:
        """Get a list of all loyalties."""
        return self._result_extract(lambda c: c.catalogs.loyalties())

    def watermarks(self) -> list[str]:
        """Get a list of all watermarks."""
        return self._result_extract(lambda c: c.catalogs.watermarks())

    def keyword_abilities(self) -> list[str]:
        """Get a list of all keyword abilities."""
        return self._result_extract(lambda c: c.catalogs.keyword_abilities())

    def keyword_actions(self) -> list[str]:
        """Get a list of all keyword actions."""
        return self._result_extract(lambda c: c.catalogs.keyword_actions())

    def ability_words(self) -> list[str]:
        """Get a list of all ability words."""
        return self._result_extract(lambda c: c.catalogs.ability_words())

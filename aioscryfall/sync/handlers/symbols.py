"""Synchronous client handler for Scryfall symbols APIs."""

from collections.abc import Iterable

from aioscryfall.models.symbols import ScryCardSymbol, ScryManaCost

from .base import BaseSyncHandler


class SymbolsSyncHandler(BaseSyncHandler):
    """ScryfallSyncClient handler for symbols APIs."""

    def all_card_symbols(self) -> Iterable[ScryCardSymbol]:
        """Get all card symbols."""
        return self._iterable_extract(lambda async_client: async_client.symbols.all_card_symbols())

    def parse_mana(self, mana_cost: str) -> ScryManaCost:
        """Parse a mana cost string."""
        return self._result_extract(
            lambda async_client: async_client.symbols.parse_mana(mana_cost)
        )

"""Client handler for the Scryfall symbols APIs."""

from collections.abc import AsyncIterable

from aioscryfall.api import symbols
from aioscryfall.models.symbols import ScryCardSymbol, ScryManaCost

from .base import BaseHandler


class SymbolsHandler(BaseHandler):
    """ScryfallClient handler for symbols APIs."""

    async def all_card_symbols(self) -> AsyncIterable[ScryCardSymbol]:
        """Get all card symbols."""
        async with self._client.limiter:
            first_page = await symbols.all_card_symbols(self._client.session)
        async for symbol in self._client.depage_list(first_page):
            yield symbol

    async def parse_mana(self, mana_cost: str) -> ScryManaCost:
        """Parse a mana cost string."""
        async with self._client.limiter:
            return await symbols.parse_mana(self._client.session, mana_cost)

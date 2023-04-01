"""Asynchronous Scryfall client."""

import asyncio
from collections.abc import AsyncIterable
from typing import TYPE_CHECKING, TypeVar

import aiolimiter

from aioscryfall.api import responses
from aioscryfall.models.lists import ScryList, ScryListable

from .handlers import bulk_data, cards, catalogs, migrations, rulings, sets, symbols

if TYPE_CHECKING:
    from aiohttp import ClientSession


_ListableT_co = TypeVar("_ListableT_co", bound=ScryListable, covariant=True)


class ScryfallClient:
    """ScryfallClient is an asynchronous client for the Scryfall API."""

    def __init__(self, session: "ClientSession") -> None:
        self.session = session
        # We limit ourselves to 10 req/s per https://scryfall.com/docs/api#rate-limits-and-good-citizenship
        self.limiter = aiolimiter.AsyncLimiter(10, 1)  # 10 requests per second

        # Mount handlers
        self.bulk_data = bulk_data.BulkDataHandler(self)
        self.cards = cards.CardsHandler(self)
        self.catalogs = catalogs.CatalogsHandler(self)
        self.migrations = migrations.MigrationsHandler(self)
        self.rulings = rulings.RulingsHandler(self)
        self.sets = sets.SetsHandler(self)
        self.symbols = symbols.SymbolsHandler(self)

    async def _get_next_page(
        self, scry_list: ScryList[_ListableT_co]
    ) -> ScryList[_ListableT_co] | None:
        """Get the next page for a ScryList."""
        if scry_list.next_page is None:
            return None

        async with self.limiter:
            async with self.session.get(scry_list.next_page) as resp:
                return await responses.read_response_payload(resp, ScryList[_ListableT_co])

    async def depage_list(
        self, paged_list: ScryList[_ListableT_co]
    ) -> AsyncIterable[_ListableT_co]:
        """Iterate over a paged list, retrieving the next page as needed."""
        current_page: ScryList[_ListableT_co] | None = paged_list
        while current_page is not None:
            next_page_task = asyncio.create_task(self._get_next_page(current_page))

            for item in current_page.data:
                yield item

            current_page = await next_page_task

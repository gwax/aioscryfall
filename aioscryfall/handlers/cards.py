"""Client handler for the Scryfall cards APIs."""

from collections.abc import AsyncIterable, Awaitable
from typing import TYPE_CHECKING, overload
from uuid import UUID

from aioscryfall.api import cards
from aioscryfall.models.cards import ScryCard

from .base import BaseHandler

if TYPE_CHECKING:
    from aioscryfall.api.cards import CardIdentifier, SortDirection, SortOrdering, UniqueMode


class CardsHandler(BaseHandler):
    """ScryfallClient handler for cards APIs."""

    async def search(
        self,
        query: str,
        *,
        unique: "UniqueMode | None" = None,
        order: "SortOrdering | None" = None,
        direction: "SortDirection | None" = None,
        include_extras: bool | None = None,
        include_multilingual: bool | None = None,
        include_variations: bool | None = None,
    ) -> AsyncIterable[ScryCard]:
        """Search for cards."""
        async with self._client.limiter:
            first_page = await cards.search(
                self._client.session,
                query,
                unique=unique,
                order=order,
                direction=direction,
                include_extras=include_extras,
                include_multilingual=include_multilingual,
                include_variations=include_variations,
            )
        async for card in self._client.depage_list(first_page):
            yield card

    @overload
    def named(self, *, exact: str, set_code: str | None = None) -> Awaitable[ScryCard]:
        ...

    @overload
    def named(self, *, fuzzy: str, set_code: str | None = None) -> Awaitable[ScryCard]:
        ...

    async def named(
        self,
        *,
        exact: str | None = None,
        fuzzy: str | None = None,
        set_code: str | None = None,
    ) -> ScryCard:
        """Get a card by name and, optionally, set."""
        has_identifier = (exact is not None, fuzzy is not None)
        invalid_args_msg = "Exactly one of exact, fuzzy must be specified."
        if len([x for x in has_identifier if x]) != 1:
            raise ValueError(invalid_args_msg)
        async with self._client.limiter:
            if exact is not None:
                return await cards.named(self._client.session, exact=exact, set_code=set_code)
            if fuzzy is not None:
                return await cards.named(self._client.session, fuzzy=fuzzy, set_code=set_code)
            raise ValueError(invalid_args_msg)

    async def autocomplete(self, query: str, *, include_extras: bool | None = None) -> list[str]:
        """Get autocomplete suggestions for a query."""
        async with self._client.limiter:
            catalog = await cards.autocomplete(
                self._client.session, query, include_extras=include_extras
            )
        return catalog.data

    async def random(self, *, query: str | None = None) -> ScryCard:
        """Get a random card."""
        async with self._client.limiter:
            return await cards.random(self._client.session, query=query)

    async def get_collection(self, identifiers: list["CardIdentifier"]) -> AsyncIterable[ScryCard]:
        """Get a collection of cards by various identifiers."""
        async with self._client.limiter:
            first_page = await cards.collection(self._client.session, identifiers)
        async for card in self._client.depage_list(first_page):
            yield card

    @overload
    def get_card(self, *, set_code: str, collector_number: str) -> Awaitable[ScryCard]:
        ...

    @overload
    def get_card(self, *, multiverse_id: int) -> Awaitable[ScryCard]:
        ...

    @overload
    def get_card(self, *, mtgo_id: int) -> Awaitable[ScryCard]:
        ...

    @overload
    def get_card(self, *, arena_id: int) -> Awaitable[ScryCard]:
        ...

    @overload
    def get_card(self, *, tcgplayer_id: int) -> Awaitable[ScryCard]:
        ...

    @overload
    def get_card(self, *, cardmarket_id: int) -> Awaitable[ScryCard]:
        ...

    @overload
    def get_card(self, *, scryfall_id: UUID) -> Awaitable[ScryCard]:
        ...

    async def get_card(
        self,
        *,
        set_code: str | None = None,
        collector_number: str | None = None,
        multiverse_id: int | None = None,
        mtgo_id: int | None = None,
        arena_id: int | None = None,
        tcgplayer_id: int | None = None,
        cardmarket_id: int | None = None,
        scryfall_id: UUID | None = None,
    ) -> ScryCard:
        """Get a single card."""
        has_identifier = (
            set_code is not None and collector_number is not None,
            multiverse_id is not None,
            mtgo_id is not None,
            arena_id is not None,
            tcgplayer_id is not None,
            cardmarket_id is not None,
            scryfall_id is not None,
        )
        invalid_args_msg = "Exactly one of (set_code and collector_number), multiverse_id, mtgo_id, arena_id, tcgplayer_id, cardmarket_id, scryfall_id must be specified."
        if len([x for x in has_identifier if x]) != 1:
            raise ValueError(invalid_args_msg)
        async with self._client.limiter:
            if set_code is not None and collector_number is not None:
                return await cards.getby_set_code_and_number(
                    self._client.session, set_code, collector_number
                )
            if multiverse_id is not None:
                return await cards.getby_multiverse_id(self._client.session, multiverse_id)
            if mtgo_id is not None:
                return await cards.getby_mtgo_id(self._client.session, mtgo_id)
            if arena_id is not None:
                return await cards.getby_arena_id(self._client.session, arena_id)
            if tcgplayer_id is not None:
                return await cards.getby_tcgplayer_id(self._client.session, tcgplayer_id)
            if cardmarket_id is not None:
                return await cards.getby_cardmarket_id(self._client.session, cardmarket_id)
            if scryfall_id is not None:
                return await cards.getby_id(self._client.session, scryfall_id)
            raise ValueError(invalid_args_msg)

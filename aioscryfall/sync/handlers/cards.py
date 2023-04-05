"""Synchronous client handler for Scryfall cards APIs."""

from collections.abc import Iterable
from typing import TYPE_CHECKING, cast, overload
from uuid import UUID

from aioscryfall.models.cards import ScryCard
from aioscryfall.models.lists import ScryListable

from .base import BaseSyncHandler

if TYPE_CHECKING:
    from aioscryfall.api.cards import CardIdentifier, SortDirection, SortOrdering, UniqueMode


class CardsSyncHandler(BaseSyncHandler):
    """ScryfallSyncClient handler for cards APIs."""

    def search(
        self,
        query: str,
        *,
        unique: "UniqueMode | None" = None,
        order: "SortOrdering | None" = None,
        direction: "SortDirection | None" = None,
        include_extras: bool | None = None,
        include_multilingual: bool | None = None,
        include_variations: bool | None = None,
    ) -> Iterable[ScryCard]:
        """Search for cards."""
        return self._iterable_extract(
            lambda c: c.cards.search(
                query,
                unique=unique,
                order=order,
                direction=direction,
                include_extras=include_extras,
                include_multilingual=include_multilingual,
                include_variations=include_variations,
            )
        )

    @overload
    def named(self, *, exact: str, set_code: str | None = None) -> ScryCard:
        ...

    @overload
    def named(self, *, fuzzy: str, set_code: str | None = None) -> ScryCard:
        ...

    def named(
        self,
        *,
        exact: str | None = None,
        fuzzy: str | None = None,
        set_code: str | None = None,
    ) -> ScryCard:
        """Get a card by name and, optionally, set."""
        invalid_args_msg = "Exactly one of exact, fuzzy must be specified."
        if exact is None and fuzzy is None:
            raise ValueError(invalid_args_msg)
        if exact is not None:
            return self._result_extract(
                # cast is necessary because of https://github.com/python/mypy/issues/2608
                lambda c: c.cards.named(exact=cast(str, exact), set_code=set_code)
            )
        if fuzzy is not None:
            return self._result_extract(
                # cast is necessary because of https://github.com/python/mypy/issues/2608
                lambda c: c.cards.named(fuzzy=cast(str, fuzzy), set_code=set_code)
            )
        raise ValueError(invalid_args_msg)

    def autocomplete(self, query: str, *, include_extras: bool | None = None) -> list[str]:
        """Get autocomplete suggestions for a query."""
        return self._result_extract(
            lambda c: c.cards.autocomplete(query, include_extras=include_extras)
        )

    def random(self) -> ScryCard:
        """Get a random card."""
        return self._result_extract(lambda c: c.cards.random())

    def get_collection(self, identifiers: list["CardIdentifier"]) -> Iterable[ScryCard]:
        """Get a collection of cards by ID."""
        return self._iterable_extract(lambda c: c.cards.get_collection(identifiers))

    @overload
    def get_card(self, *, set_code: str, collector_number: str) -> ScryCard:
        ...

    @overload
    def get_card(self, *, multiverse_id: int) -> ScryCard:
        ...

    @overload
    def get_card(self, *, mtgo_id: int) -> ScryCard:
        ...

    @overload
    def get_card(self, *, arena_id: int) -> ScryCard:
        ...

    @overload
    def get_card(self, *, tcgplayer_id: int) -> ScryCard:
        ...

    @overload
    def get_card(self, *, cardmarket_id: int) -> ScryCard:
        ...

    @overload
    def get_card(self, *, scryfall_id: UUID) -> ScryCard:
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
        if set_code is not None and collector_number is not None:
            return self._result_extract(
                lambda c: c.cards.get_card(
                    set_code=cast(str, set_code), collector_number=cast(str, collector_number)
                )
            )
        if multiverse_id is not None:
            return self._result_extract(
                lambda c: c.cards.get_card(multiverse_id=cast(int, multiverse_id))
            )
        if mtgo_id is not None:
            return self._result_extract(lambda c: c.cards.get_card(mtgo_id=cast(int, mtgo_id)))
        if arena_id is not None:
            return self._result_extract(lambda c: c.cards.get_card(arena_id=cast(int, arena_id)))
        if tcgplayer_id is not None:
            return self._result_extract(
                lambda c: c.cards.get_card(tcgplayer_id=cast(int, tcgplayer_id))
            )
        if cardmarket_id is not None:
            return self._result_extract(
                lambda c: c.cards.get_card(cardmarket_id=cast(int, cardmarket_id))
            )
        if scryfall_id is not None:
            return self._result_extract(
                lambda c: c.cards.get_card(scryfall_id=cast(UUID, scryfall_id))
            )
        raise ValueError(invalid_args_msg)

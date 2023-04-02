"""Client handler for the Scryfall rulings APIs."""

from collections.abc import AsyncIterable
from typing import Any, TypeVar, overload
from uuid import UUID

from aioscryfall.api import rulings
from aioscryfall.models.rulings import ScryRuling

from .base import BaseHandler


class RulingsHandler(BaseHandler):
    """ScryfallClient handler for rulings APIs."""

    @overload
    def get_rulings(self, *, card_id: UUID) -> AsyncIterable[ScryRuling]:
        ...

    @overload
    def get_rulings(self, *, multiverse_id: int) -> AsyncIterable[ScryRuling]:
        ...

    @overload
    def get_rulings(self, *, mtgo_id: int) -> AsyncIterable[ScryRuling]:
        ...

    @overload
    def get_rulings(self, *, arena_id: int) -> AsyncIterable[ScryRuling]:
        ...

    @overload
    def get_rulings(self, *, set_code: str, collector_number: str) -> AsyncIterable[ScryRuling]:
        ...

    async def get_rulings(
        self,
        *,
        card_id: UUID | None = None,
        multiverse_id: int | None = None,
        mtgo_id: int | None = None,
        arena_id: int | None = None,
        set_code: str | None = None,
        collector_number: str | None = None,
    ) -> AsyncIterable[ScryRuling]:
        """Get rulings for a card."""
        has_identifier = (
            card_id is not None,
            multiverse_id is not None,
            mtgo_id is not None,
            arena_id is not None,
            set_code is not None and collector_number is not None,
        )
        invalid_args_msg = "Exactly one of card_id, multiverse_id, mtgo_id, arena_id, (set_code and collector_number) must be specified."
        if len([x for x in has_identifier if x]) != 1:
            raise ValueError(invalid_args_msg)
        async with self._client.limiter:
            if card_id is not None:
                first_page = await rulings.getby_card_id(self._client.session, card_id)
            elif multiverse_id is not None:
                first_page = await rulings.getby_multiverse_id(self._client.session, multiverse_id)
            elif mtgo_id is not None:
                first_page = await rulings.getby_mtgo_id(self._client.session, mtgo_id)
            elif arena_id is not None:
                first_page = await rulings.getby_arena_id(self._client.session, arena_id)
            elif set_code is not None and collector_number is not None:
                first_page = await rulings.getby_set_code_and_number(
                    self._client.session, set_code, collector_number
                )
            else:
                raise ValueError(invalid_args_msg)

        async for ruling in self._client.depage_list(first_page):
            yield ruling

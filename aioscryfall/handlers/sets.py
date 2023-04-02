"""Client handler for the Scryfall sets APIs."""

from collections.abc import AsyncIterable, Awaitable
from typing import overload
from uuid import UUID

from aioscryfall.api import sets
from aioscryfall.models.sets import ScrySet

from .base import BaseHandler


class SetsHandler(BaseHandler):
    """ScryfallClient handler for sets APIs."""

    async def all_sets(self) -> AsyncIterable[ScrySet]:
        """Get all sets."""
        async with self._client.limiter:
            first_page = await sets.all_sets(self._client.session)
        async for set_ in self._client.depage_list(first_page):
            yield set_

    @overload
    def get_set(self, *, set_code: str) -> Awaitable[ScrySet]:
        ...

    @overload
    def get_set(self, *, tcgplayer_id: int) -> Awaitable[ScrySet]:
        ...

    @overload
    def get_set(self, *, scryfall_id: UUID) -> Awaitable[ScrySet]:
        ...

    async def get_set(
        self,
        *,
        set_code: str | None = None,
        tcgplayer_id: int | None = None,
        scryfall_id: UUID | None = None,
    ) -> ScrySet:
        """Get a set by its code, TCGPlayer ID, or Scryfall ID."""
        has_identifier = (
            set_code is not None,
            tcgplayer_id is not None,
            scryfall_id is not None,
        )
        invalid_args_msg = "Exactly one of set_code, tcgplayer_id, scryfall_id must be specified."
        if len([x for x in has_identifier if x]) != 1:
            raise ValueError(invalid_args_msg)
        async with self._client.limiter:
            if set_code is not None:
                return await sets.getby_code(self._client.session, set_code)
            if tcgplayer_id is not None:
                return await sets.getby_tcgplayer_id(self._client.session, tcgplayer_id)
            if scryfall_id is not None:
                return await sets.getby_id(self._client.session, scryfall_id)
            raise ValueError(invalid_args_msg)

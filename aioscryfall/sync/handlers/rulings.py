"""Synchronous client handler for Scryfall rulings APIs."""

from typing import TYPE_CHECKING, cast, overload

from .base import BaseSyncHandler

if TYPE_CHECKING:
    from collections.abc import Iterable
    from uuid import UUID

    from aioscryfall.models.rulings import ScryRuling


class RulingsSyncHandler(BaseSyncHandler):
    """ScryfallSyncClient handler for rulings APIs."""

    @overload
    def get_rulings(self, *, card_id: "UUID") -> "Iterable[ScryRuling]":
        ...

    @overload
    def get_rulings(self, *, multiverse_id: int) -> "Iterable[ScryRuling]":
        ...

    @overload
    def get_rulings(self, *, mtgo_id: int) -> "Iterable[ScryRuling]":
        ...

    @overload
    def get_rulings(self, *, arena_id: int) -> "Iterable[ScryRuling]":
        ...

    @overload
    def get_rulings(self, *, set_code: str, collector_number: str) -> "Iterable[ScryRuling]":
        ...

    def get_rulings(
        self,
        *,
        card_id: "UUID | None" = None,
        multiverse_id: int | None = None,
        mtgo_id: int | None = None,
        arena_id: int | None = None,
        set_code: str | None = None,
        collector_number: str | None = None,
    ) -> "Iterable[ScryRuling]":
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
        if card_id is not None:
            return self._iterable_extract(
                # cast is necessary because of https://github.com/python/mypy/issues/2608
                lambda c: c.rulings.get_rulings(card_id=cast(UUID, card_id))
            )
        if multiverse_id is not None:
            return self._iterable_extract(
                # cast is necessary because of https://github.com/python/mypy/issues/2608
                lambda c: c.rulings.get_rulings(multiverse_id=cast(int, multiverse_id))
            )
        if mtgo_id is not None:
            return self._iterable_extract(
                # cast is necessary because of https://github.com/python/mypy/issues/2608
                lambda c: c.rulings.get_rulings(mtgo_id=cast(int, mtgo_id))
            )
        if arena_id is not None:
            return self._iterable_extract(
                # cast is necessary because of https://github.com/python/mypy/issues/2608
                lambda c: c.rulings.get_rulings(arena_id=cast(int, arena_id))
            )
        if set_code is not None and collector_number is not None:
            return self._iterable_extract(
                lambda c: c.rulings.get_rulings(
                    # cast is necessary because of https://github.com/python/mypy/issues/2608
                    set_code=cast(str, set_code),
                    collector_number=cast(str, collector_number),
                )
            )
        raise ValueError(invalid_args_msg)

"""Synchronous client handler for Scryfall rulings APIs."""

from typing import TYPE_CHECKING, overload

from .base import BaseSyncHandler

if TYPE_CHECKING:
    from collections.abc import AsyncIterable, Callable, Iterable
    from uuid import UUID

    from aioscryfall.client import ScryfallClient
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

        # TODO: simplify after https://github.com/python/mypy/issues/14997
        def _card_id_extractor(
            id_: "UUID",
        ) -> "Callable[[ScryfallClient], AsyncIterable[ScryRuling]]":
            def _extractor(async_client: "ScryfallClient") -> "AsyncIterable[ScryRuling]":
                return async_client.rulings.get_rulings(card_id=id_)

            return _extractor

        def _multiverse_id_extractor(
            id_: int,
        ) -> "Callable[[ScryfallClient], AsyncIterable[ScryRuling]]":
            def _extractor(async_client: "ScryfallClient") -> "AsyncIterable[ScryRuling]":
                return async_client.rulings.get_rulings(multiverse_id=id_)

            return _extractor

        def _mtgo_id_extractor(
            id_: int,
        ) -> "Callable[[ScryfallClient], AsyncIterable[ScryRuling]]":
            def _extractor(async_client: "ScryfallClient") -> "AsyncIterable[ScryRuling]":
                return async_client.rulings.get_rulings(mtgo_id=id_)

            return _extractor

        def _arena_id_extractor(
            id_: int,
        ) -> "Callable[[ScryfallClient], AsyncIterable[ScryRuling]]":
            def _extractor(async_client: "ScryfallClient") -> "AsyncIterable[ScryRuling]":
                return async_client.rulings.get_rulings(arena_id=id_)

            return _extractor

        def _set_code_collector_number_extractor(
            set_code: str, collector_number: str
        ) -> "Callable[[ScryfallClient], AsyncIterable[ScryRuling]]":
            def _extractor(async_client: "ScryfallClient") -> "AsyncIterable[ScryRuling]":
                return async_client.rulings.get_rulings(
                    set_code=set_code, collector_number=collector_number
                )

            return _extractor

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
            return self._iterable_extract(_card_id_extractor(card_id))
        if multiverse_id is not None:
            return self._iterable_extract(_multiverse_id_extractor(multiverse_id))
        if mtgo_id is not None:
            return self._iterable_extract(_mtgo_id_extractor(mtgo_id))
        if arena_id is not None:
            return self._iterable_extract(_arena_id_extractor(arena_id))
        if set_code is not None and collector_number is not None:
            return self._iterable_extract(
                _set_code_collector_number_extractor(set_code, collector_number)
            )
        raise ValueError(invalid_args_msg)

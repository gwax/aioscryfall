"""Synchronous client handler for Scryfall bulk data APIs."""

from collections.abc import Iterable
from typing import TYPE_CHECKING, overload
from uuid import UUID

from aioscryfall.models.bulk_data import ScryBulkData
from aioscryfall.models.lists import ScryListable

from .base import BaseSyncHandler

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aioscryfall.client import ScryfallClient


class BulkDataSyncHandler(BaseSyncHandler):
    """ScryfallSyncClient handler for bulk_data APIs."""

    def all_bulk_data(self) -> Iterable[ScryBulkData]:
        """Get all bulk data."""
        return self._iterable_extract(lambda c: c.bulk_data.all_bulk_data())

    @overload
    def get_bulk_data(self, *, bulk_data_id: UUID) -> ScryBulkData:
        ...

    @overload
    def get_bulk_data(self, *, bulk_data_type: str) -> ScryBulkData:
        ...

    def get_bulk_data(
        self,
        *,
        bulk_data_id: UUID | None = None,
        bulk_data_type: str | None = None,
    ) -> ScryBulkData:
        """Get a single bulk data item."""

        def _id_extractor(id_: UUID) -> "Callable[[ScryfallClient], Awaitable[ScryBulkData]]":
            def _extractor(async_client: "ScryfallClient") -> "Awaitable[ScryBulkData]":
                return async_client.bulk_data.get_bulk_data(bulk_data_id=id_)

            return _extractor

        def _type_extractor(type_: str) -> "Callable[[ScryfallClient], Awaitable[ScryBulkData]]":
            def _extractor(async_client: "ScryfallClient") -> "Awaitable[ScryBulkData]":
                return async_client.bulk_data.get_bulk_data(bulk_data_type=type_)

            return _extractor

        invalid_args_msg = "Exactly one of bulk_data_id, bulk_data_type must be specified."
        if bulk_data_id is None and bulk_data_type is None:
            raise ValueError(invalid_args_msg)
        if bulk_data_id is not None:
            return self._result_extract(_id_extractor(bulk_data_id))
        if bulk_data_type is not None:
            return self._result_extract(_type_extractor(bulk_data_type))
        raise ValueError(invalid_args_msg)

    def fetch_contents(self, bulk_data_item: ScryBulkData) -> list[ScryListable]:
        """Fetch the contents of a bulk data item."""
        return self._result_extract(lambda c: c.bulk_data.fetch_contents(bulk_data_item))

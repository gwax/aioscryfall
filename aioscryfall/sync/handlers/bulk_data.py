"""Synchronous client handler for Scryfall bulk data APIs."""

from collections.abc import Iterable
from typing import cast, overload
from uuid import UUID

from aioscryfall.models.bulk_data import ScryBulkData
from aioscryfall.models.lists import ScryListable

from .base import BaseSyncHandler


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
        invalid_args_msg = "Exactly one of bulk_data_id, bulk_data_type must be specified."
        if bulk_data_id is None and bulk_data_type is None:
            raise ValueError(invalid_args_msg)
        if bulk_data_id is not None:
            return self._result_extract(
                # cast is necessary because of https://github.com/python/mypy/issues/2608
                lambda c: c.bulk_data.get_bulk_data(bulk_data_id=cast(UUID, bulk_data_id))
            )
        if bulk_data_type is not None:
            return self._result_extract(
                # cast is necessary because of https://github.com/python/mypy/issues/2608
                lambda c: c.bulk_data.get_bulk_data(bulk_data_type=cast(str, bulk_data_type))
            )
        raise ValueError(invalid_args_msg)

    def fetch_contents(self, bulk_data_item: ScryBulkData) -> list[ScryListable]:
        """Fetch the contents of a bulk data item."""
        return self._result_extract(lambda c: c.bulk_data.fetch_contents(bulk_data_item))

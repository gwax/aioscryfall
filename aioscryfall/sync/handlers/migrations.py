"""Synchronous client handler for Scryfall migrations APIs."""

from collections.abc import Iterable
from uuid import UUID

from aioscryfall.models.migrations import ScryMigration

from .base import BaseSyncHandler


class MigrationsSyncHandler(BaseSyncHandler):
    """ScryfallSyncClient handler for symbols APIs."""

    def all_migrations(self) -> Iterable[ScryMigration]:
        """Get all migrations."""
        return self._iterable_extract(lambda c: c.migrations.all_migrations())

    def get_migration(self, *, migration_id: UUID) -> ScryMigration:
        """Get a migration by its ID."""
        return self._result_extract(
            lambda c: c.migrations.get_migration(migration_id=migration_id)
        )

"""Client handler for the Scryfall migrations APIs."""

from collections.abc import AsyncIterable
from uuid import UUID

from aioscryfall.api import migrations
from aioscryfall.models.migrations import ScryMigration

from .base import BaseHandler


class MigrationsHandler(BaseHandler):
    """ScryfallClient handler for migrations APIs."""

    async def all_migrations(self) -> AsyncIterable[ScryMigration]:
        """Get all migrations."""
        async with self._client.limiter:
            first_page = await migrations.all_migrations(self._client.session)
        async for migration in self._client.depage_list(first_page):
            yield migration

    async def get_migration(self, *, migration_id: UUID) -> ScryMigration:
        """Get a migration by its ID."""
        async with self._client.limiter:
            return await migrations.getby_id(self._client.session, migration_id)

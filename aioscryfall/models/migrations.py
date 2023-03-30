"""Models for https://scryfall.com/docs/api/migrations objects."""

import datetime as dt
from enum import Enum
from uuid import UUID

from msgspec import Struct


class ScryMigrationStrategy(str, Enum):
    """A ScrymigrationStrategy represents the strategy used to migrate a card object to a new object."""

    MERGE = "merge"
    DELETE = "delete"


class ScryMigration(
    Struct, tag_field="object", tag="migration", kw_only=True, rename={"id_": "id"}
):
    """A ScryMigration represents information about a card object that has been migrated to a new object."""

    id_: UUID
    uri: str
    performed_at: dt.date
    migration_strategy: ScryMigrationStrategy
    old_scryfall_id: UUID
    new_scryfall_id: UUID | None = None
    note: str | None = None

"""Models for https://scryfall.com/docs/api/bulk-data objects."""

import datetime as dt
from uuid import UUID

from msgspec import Struct


class ScryBulkData(
    Struct,
    tag_field="object",
    tag="bulk_data",
    kw_only=True,
    omit_defaults=True,
    rename={"id_": "id", "type_": "type"},
):
    """A ScryBulkData represents a daily exports of Scryfall data in bulk files."""

    id_: UUID
    uri: str
    type_: str
    name: str
    description: str
    download_uri: str
    updated_at: dt.datetime
    compressed_size: int | None = None
    content_type: str
    content_encoding: str

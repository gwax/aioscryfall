"""Models for https://scryfall.com/docs/api/rulings objects."""

import datetime as dt
from uuid import UUID

from msgspec import Struct


class ScryRuling(Struct, tag_field="object", tag="ruling", kw_only=True, omit_defaults=True):
    """A ScryRuling represent Oracle rulings, Wizards of the Coast set release notes, or Scryfall notes for a particular card."""

    oracle_id: UUID
    source: str
    published_at: dt.date
    comment: str

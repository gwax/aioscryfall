"""Models for https://scryfall.com/docs/api/lists objects."""

import dataclasses
from typing import Generic, Self, TypeAlias, TypeVar, cast

from msgspec import Struct

from .bulk_data import ScryBulkData
from .cards import ScryCard
from .catalogs import ScryCatalog
from .migrations import ScryMigration
from .rulings import ScryRuling
from .sets import ScrySet
from .symbols import ScryCardSymbol, ScryManaCost

ScryListable: TypeAlias = (
    ScryBulkData
    | ScryCard
    | ScryCardSymbol
    | ScryCatalog
    | ScryManaCost
    | ScryMigration
    | ScryRuling
    | ScrySet
)


class RawScryList(Struct, tag_field="object", tag="list", kw_only=True):
    """A RawScryList object represents an untyped, requested sequence of other objects.

    Due to a lack of support for generics in msgspec, this class is used for decoding
    of all possible list types, even if we might know the type of the list elements.
    """

    data: list[ScryListable]
    has_more: bool | None = None
    next_page: str | None = None
    total_cards: int | None = None
    warnings: list[str] | None = None


_T = TypeVar("_T", bound=ScryListable)


@dataclasses.dataclass(kw_only=True)
class ScryList(Generic[_T]):
    """A ScryList object represents a typed, requested sequence of other objects.

    This class is a wrapper around RawScryList that provides the ability to specify
    static type information at time of writing.
    """

    data: list[_T]
    has_more: bool | None = None
    next_page: str | None = None
    total_cards: int | None = None
    warnings: list[str] | None = None

    @classmethod
    def from_raw(cls, raw: RawScryList) -> Self:
        """Create a typed ScryList from a RawScryList."""
        return cls(
            data=cast(list[_T], raw.data),
            has_more=raw.has_more,
            next_page=raw.next_page,
            total_cards=raw.total_cards,
            warnings=raw.warnings,
        )

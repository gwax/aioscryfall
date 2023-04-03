"""Models for https://scryfall.com/docs/api/catalog objects."""

from msgspec import Struct


class ScryCatalog(Struct, tag_field="object", tag="catalog", kw_only=True, omit_defaults=True):
    """A ScryCatalog object contains an array of Magic datapoints."""

    uri: str | None = None
    total_values: int
    data: list[str]

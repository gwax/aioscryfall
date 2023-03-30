"""Model for https://scryfall.com/docs/api/errors objects."""

from msgspec import Struct


class ScryError(Struct, tag_field="object", tag="error", kw_only=True, rename={"type_": "type"}):
    """A ScryError object represents a failure to find information or understand the input you provided to the API."""

    status: int
    code: str
    details: str
    type_: str | None = None
    warnings: list[str] | None = None

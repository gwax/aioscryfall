"""Models for https://scryfall.com/docs/api/card-symbols objects."""

from msgspec import Struct

from .common import ScryColor


class ScryCardSymbol(
    Struct, tag_field="object", tag="card_symbol", kw_only=True, omit_defaults=True
):
    """ScryCardSymbol represent illustrated symbols from a card's mana cost or Oracle text."""

    symbol: str
    loose_variant: str | None = None
    english: str
    transposable: bool
    represents_mana: bool
    mana_value: float | None = None
    appears_in_mana_costs: bool
    funny: bool
    colors: list[ScryColor]
    gatherer_alternates: list[str] | None = None
    svg_uri: str | None = None


class ScryManaCost(Struct, tag_field="object", tag="mana_cost", kw_only=True, omit_defaults=True):
    """ScryManaCost object represents a canonicalized mana cost."""

    cost: str
    cmc: float
    colors: list[ScryColor]
    colorless: bool
    monocolored: bool
    multicolored: bool

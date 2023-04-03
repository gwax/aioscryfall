"""Models for https://scryfall.com/docs/api/sets objects."""

import datetime as dt
from enum import Enum
from uuid import UUID

from msgspec import Struct


class ScrySetType(str, Enum):
    """An exhaustive list of set_types."""

    CORE = "core"
    EXPANSION = "expansion"
    MASTERS = "masters"
    MASTERPIECE = "masterpiece"
    FROM_THE_VAULT = "from_the_vault"
    SPELLBOOK = "spellbook"
    PREMIUM_DECK = "premium_deck"
    DUEL_DECK = "duel_deck"
    DRAFT_INNOVATION = "draft_innovation"
    TREASURE_CHEST = "treasure_chest"
    COMMANDER = "commander"
    PLANECHASE = "planechase"
    ARCHENEMY = "archenemy"
    VANGUARD = "vanguard"
    FUNNY = "funny"
    STARTER = "starter"
    BOX = "box"
    PROMO = "promo"
    TOKEN = "token"
    MEMORABILIA = "memorabilia"
    ALCHEMY = "alchemy"
    ARSENAL = "arsenal"
    MINIGAME = "minigame"


class ScrySet(
    Struct, tag_field="object", tag="set", kw_only=True, omit_defaults=True, rename={"id_": "id"}
):
    """A ScrySet object represents a group of related Magic cards."""

    id_: UUID
    code: str
    mtgo_code: str | None = None
    arena_code: str | None = None
    tcgplayer_id: int | None = None
    name: str
    set_type: ScrySetType
    released_at: dt.date | None = None
    block_code: str | None = None
    block: str | None = None
    parent_set_code: str | None = None
    card_count: int
    printed_size: int | None = None
    digital: bool
    foil_only: bool
    nonfoil_only: bool | None = None
    icon_svg_uri: str
    search_uri: str
    scryfall_uri: str
    uri: str

"""Scryfall object models."""

import dataclasses
import datetime as dt
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Generic, TypeAlias, TypeVar, cast
from uuid import UUID

from msgspec import Struct

if TYPE_CHECKING:
    from typing import Self


class Color(str, Enum):
    """Enum for https://scryfall.com/docs/api/colors#color-arrays"""

    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"
    COLORLESS = "C"
    TAP = "T"


class SetType(str, Enum):
    """Enum for https://scryfall.com/docs/api/sets#set-types"""

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


class CardLayout(str, Enum):
    """Enum for https://scryfall.com/docs/api/layouts#layout"""

    NORMAL = "normal"
    SPLIT = "split"
    FLIP = "flip"
    TRANSFORM = "transform"
    MODAL_DFC = "modal_dfc"
    MELD = "meld"
    LEVELER = "leveler"
    CLASS = "class"
    SAGA = "saga"
    ADVENTURE = "adventure"
    PLANAR = "planar"
    SCHEME = "scheme"
    VANGUARD = "vanguard"
    TOKEN = "token"
    DOUBLE_FACED_TOKEN = "double_faced_token"
    EMBLEM = "emblem"
    AUGMENT = "augment"
    HOST = "host"
    ART_SERIES = "art_series"
    DOUBLE_SIDED = "double_sided"
    REVERSIBLE_CARD = "reversible_card"


class CardFrame(str, Enum):
    """Enum for https://scryfall.com/docs/api/layouts#frames"""

    Y1993 = "1993"
    Y1997 = "1997"
    Y2003 = "2003"
    Y2015 = "2015"
    FUTURE = "future"


class FrameEffect(str, Enum):
    """Enum for https://scryfall.com/docs/api/layouts#frame-effects"""

    NONE = ""
    LEGENDARY = "legendary"
    MIRACLE = "miracle"
    NYXBORN = "nyxborn"
    NYXTOUCHED = "nyxtouched"
    DRAFT = "draft"
    DEVOID = "devoid"
    TOMBSTONE = "tombstone"
    COLORSHIFTED = "colorshifted"
    INVERTED = "inverted"
    SUNMOONDFC = "sunmoondfc"
    COMPASSLANDDFC = "compasslanddfc"
    ORIGINPWDFC = "originpwdfc"
    MOONELDRAZIDFC = "mooneldrazidfc"
    MOONREVERSEMOONDFC = "moonreversemoondfc"
    WAXINGANDWANINGMOONDFC = "waxingandwaningmoondfc"
    SHOWCASE = "showcase"
    EXTENDEDART = "extendedart"
    COMPANION = "companion"
    FULLART = "fullart"
    ETCHED = "etched"
    SNOW = "snow"
    LESSON = "lesson"
    TEXTLESS = "textless"
    SHATTEREDGLASS = "shatteredglass"
    CONVERTDFC = "convertdfc"
    FANDFC = "fandfc"
    UPSIDEDOWNDFC = "upsidedowndfc"
    GILDED = "gilded"


class BorderColor(str, Enum):
    """Enum for card border_color"""

    BLACK = "black"
    BORDERLESS = "borderless"
    GOLD = "gold"
    SILVER = "silver"
    WHITE = "white"


class Finish(str, Enum):
    """Enum for card finishes"""

    FOIL = "foil"
    NONFOIL = "nonfoil"
    ETCHED = "etched"
    GLOSSY = "glossy"


class ImageStatus(str, Enum):
    """Enum for card image_status"""

    MISSING = "missing"
    PLACEHOLDER = "placeholder"
    LOWRES = "lowres"
    HIGHRES_SCAN = "highres_scan"


class Game(str, Enum):
    """Enum for card games"""

    PAPER = "paper"
    ARENA = "arena"
    MTGO = "mtgo"
    SEGA = "sega"
    ASTRAL = "astral"


class Rarity(str, Enum):
    """Enum for card rarity"""

    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    MYTHIC = "mythic"
    SPECIAL = "special"
    BONUS = "bonus"


class SecurityStamp(str, Enum):
    """Enum for card security_stamp"""

    OVAL = "oval"
    TRIANGLE = "triangle"
    ACORN = "acorn"
    ARENA = "arena"
    CIRCLE = "circle"
    HEART = "heart"


class Format(str, Enum):
    """Enum for card legalities keys"""

    BRAWL = "brawl"
    COMMANDER = "commander"
    DUEL = "duel"
    FRONTIER = "frontier"
    FUTURE = "future"
    LEGACY = "legacy"
    MODERN = "modern"
    OLDSCHOOL = "oldschool"
    PAUPER = "pauper"
    PENNY = "penny"
    STANDARD = "standard"
    VINTAGE = "vintage"
    HISTORIC = "historic"
    PIONEER = "pioneer"
    GLADIATOR = "gladiator"
    EXPLORER = "explorer"
    HISTORICBRAWL = "historicbrawl"
    ALCHEMY = "alchemy"
    PAUPERCOMMANDER = "paupercommander"
    PREMODERN = "premodern"
    PREDH = "predh"
    OATHBREAKER = "oathbreaker"


class Legality(str, Enum):
    """Enum for card legalities values"""

    LEGAL = "legal"
    NOT_LEGAL = "not_legal"
    RESTRICTED = "restricted"
    BANNED = "banned"


class MigrationStrategy(str, Enum):
    """Enum for migration strategy values"""

    MERGE = "merge"
    DELETE = "delete"


class Error(Struct, tag_field="object", tag="error", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/errors"""

    status: int
    code: str
    details: str
    type: str | None = None
    warnings: list[str] | None = None


class Set(Struct, tag_field="object", tag="set", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/sets"""

    id: UUID
    code: str
    mtgo_code: str | None = None
    arena_code: str | None = None
    tcgplayer_id: int | None = None
    name: str
    set_type: SetType
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


class RelatedCard(
    Struct, tag_field="object", tag="related_card", kw_only=True, omit_defaults=True
):
    """Model for https://scryfall.com/docs/api/cards#related-card-objects"""

    id: UUID
    component: str
    name: str
    type_line: str
    uri: str


class CardFace(Struct, tag_field="object", tag="card_face", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/cards#card-face-objects"""

    artist: str | None = None
    artist_id: UUID | None = None
    cmc: float | None = None
    color_indicator: list[Color] | None = None
    colors: list[Color] | None = None
    flavor_name: str | None = None
    flavor_text: str | None = None
    illustration_id: UUID | None = None
    image_uris: dict[str, str] | None = None
    layout: CardLayout | None = None
    loyalty: str | None = None
    mana_cost: str
    name: str
    oracle_id: UUID | None = None
    oracle_text: str | None = None
    power: str | None = None
    printed_name: str | None = None
    printed_text: str | None = None
    printed_type_line: str | None = None
    toughness: str | None = None
    type_line: str | None = None
    watermark: str | None = None


class CardPreviewBlock(Struct):
    """Model for card preview block."""

    source: str
    source_uri: str
    previewed_at: dt.date


class Card(Struct, tag_field="object", tag="card", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/cards"""

    # Core Card Fields
    arena_id: int | None = None
    id: UUID
    lang: str
    mtgo_id: int | None = None
    mtgo_foil_id: int | None = None
    multiverse_ids: list[int] | None = None
    tcgplayer_id: int | None = None
    tcgplayer_etched_id: int | None = None
    cardmarket_id: int | None = None
    oracle_id: UUID | None = None
    prints_search_uri: str
    rulings_uri: str
    scryfall_uri: str
    uri: str
    # Gameplay Fields
    all_parts: list[RelatedCard] | None = None
    card_faces: list[CardFace] | None = None
    cmc: float | None = None
    colors: list[Color] | None = None
    color_identity: list[Color]
    color_indicator: list[Color] | None = None
    edhrec_rank: int | None = None
    foil: bool
    hand_modifier: str | None = None
    keywords: list[str]
    layout: CardLayout
    legalities: dict[Format, Legality]
    life_modifier: str | None = None
    loyalty: str | None = None
    mana_cost: str | None = None
    name: str
    nonfoil: bool
    oracle_text: str | None = None
    oversized: bool
    penny_rank: int | None = None
    power: str | None = None
    produced_mana: list[str] | None = None
    reserved: bool
    toughness: str | None = None
    type_line: str | None = None
    # Print Fields
    artist: str | None = None
    artist_ids: list[UUID] | None = None
    booster: bool
    border_color: BorderColor
    card_back_id: UUID | None = None
    collector_number: str
    content_warning: bool | None = None
    digital: bool
    finishes: list[Finish]
    flavor_name: str | None = None
    flavor_text: str | None = None
    frame_effect: FrameEffect | None = None
    frame_effects: list[FrameEffect] | None = None
    frame: CardFrame
    full_art: bool
    games: list[Game]
    highres_image: bool
    illustration_id: UUID | None = None
    image_status: ImageStatus
    image_uris: dict[str, str] | None = None
    prices: dict[str, Decimal | None] | None  # TODO: enum keys=None
    printed_name: str | None = None
    printed_text: str | None = None
    printed_type_line: str | None = None
    promo: bool
    promo_types: list[str] | None = None
    purchase_uris: dict[str, str] | None = None
    rarity: Rarity
    related_uris: dict[str, str] | None = None
    released_at: dt.date
    reprint: bool
    scryfall_set_uri: str
    set_name: str
    set_search_uri: str
    set_type: str
    set_uri: str
    set: str
    set_id: UUID
    story_spotlight: bool
    textless: bool
    variation: bool
    variation_of: UUID | None = None
    security_stamp: SecurityStamp | None = None
    watermark: str | None = None
    preview: CardPreviewBlock | None = None


class BulkData(Struct, tag_field="object", tag="bulk_data", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/bulk-data"""

    id: UUID
    uri: str
    type: str
    name: str
    description: str
    download_uri: str
    updated_at: dt.datetime
    compressed_size: int | None = None
    content_type: str
    content_encoding: str


class Migration(Struct, tag_field="object", tag="migration", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/migrations"""

    id: UUID
    uri: str
    performed_at: dt.date
    migration_strategy: MigrationStrategy
    old_scryfall_id: UUID
    new_scryfall_id: UUID | None = None
    note: str | None = None


class Catalog(Struct, tag_field="object", tag="catalog", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/catalog"""

    uri: str | None = None
    total_values: int
    data: list[str]


class Ruling(Struct, tag_field="object", tag="ruling", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/rulings"""

    oracle_id: UUID
    source: str
    published_at: dt.date
    comment: str


class CardSymbol(Struct, tag_field="object", tag="card_symbol", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/card-symbols"""

    symbol: str
    loose_variant: str | None = None
    english: str
    transposable: bool
    represents_mana: bool
    mana_value: float | None = None
    appears_in_mana_costs: bool
    funny: bool
    colors: list[Color]
    gatherer_alternates: list[str] | None = None
    svg_uri: str | None = None


class ManaCost(Struct, tag_field="object", tag="mana_cost", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/card-symbols/parse-mana"""

    cost: str
    cmc: float
    colors: list[Color]
    colorless: bool
    monocolored: bool
    multicolored: bool


Listable: TypeAlias = Set | Card | BulkData | Migration | Ruling | CardSymbol


class RawList(Struct, tag_field="object", tag="list", kw_only=True, omit_defaults=True):
    """Model for https://scryfall.com/docs/api/lists"""

    data: list[Listable]
    has_more: bool | None = None
    next_page: str | None = None
    total_cards: int | None = None
    warnings: list[str] | None = None


T = TypeVar("T")


@dataclasses.dataclass(kw_only=True)
class List(Generic[T]):
    """Typed variant of RawList for improved type checking."""

    data: list[T]
    has_more: bool | None = None
    next_page: str | None
    total_cards: int | None
    warnings: list[str] | None

    @classmethod
    def from_raw(cls, raw: RawList) -> "Self":
        """Convert a RawList to a typed List."""
        return cls(
            data=cast(list[T], raw.data),
            has_more=raw.has_more,
            next_page=raw.next_page,
            total_cards=raw.total_cards,
            warnings=raw.warnings,
        )

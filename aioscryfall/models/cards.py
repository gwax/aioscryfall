"""Models for https://scryfall.com/docs/api/cards objects."""

import datetime as dt
from decimal import Decimal
from enum import Enum
from uuid import UUID

from msgspec import Struct

from .common import ScryColor, ScryGame


class ScryCardLayout(str, Enum):
    """ScryCardLayout represents the layout of a card.

    See: https://scryfall.com/docs/api/layouts#layout
    """

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


class ScryCardFrame(str, Enum):
    """ScryCardFrame represents the frame of a card.

    See: https://scryfall.com/docs/api/layouts#frames
    """

    Y1993 = "1993"
    Y1997 = "1997"
    Y2003 = "2003"
    Y2015 = "2015"
    FUTURE = "future"


class ScryCardFrameEffect(str, Enum):
    """ScryCardFrameEffect represents the frame effects on a card.

    See: https://scryfall.com/docs/api/layouts#frame-effects
    """

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


class ScryCardBorderColor(str, Enum):
    """A ScryCardBorderColor represents the border color of a card."""

    BLACK = "black"
    BORDERLESS = "borderless"
    GOLD = "gold"
    SILVER = "silver"
    WHITE = "white"


class ScryCardFinish(str, Enum):
    """ScryCardFinish represents the finish effects on a card."""

    FOIL = "foil"
    NONFOIL = "nonfoil"
    ETCHED = "etched"
    GLOSSY = "glossy"


class ScryCardImageStatus(str, Enum):
    """ScryCardImageStatus represents the state of a card's image file on Scryfall servers."""

    MISSING = "missing"
    PLACEHOLDER = "placeholder"
    LOWRES = "lowres"
    HIGHRES_SCAN = "highres_scan"


class ScryCardRarity(str, Enum):
    """ScryCardRarity represents a card's rarity."""

    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    MYTHIC = "mythic"
    SPECIAL = "special"
    BONUS = "bonus"


class ScryCardSecurityStamp(str, Enum):
    """ScryCardSecurityStamp represents the security stamp on a card, if any."""

    OVAL = "oval"
    TRIANGLE = "triangle"
    ACORN = "acorn"
    ARENA = "arena"
    CIRCLE = "circle"
    HEART = "heart"


class ScryCardLegality(str, Enum):
    """ScryCardLegality described the legality of a card for a given format."""

    LEGAL = "legal"
    NOT_LEGAL = "not_legal"
    RESTRICTED = "restricted"
    BANNED = "banned"


class ScryRelatedCard(
    Struct, tag_field="object", tag="related_card", kw_only=True, rename={"id_": "id"}
):
    """A ScryRelatedCard represents a closely related card."""

    id_: UUID
    component: str
    name: str
    type_line: str
    uri: str


class ScryCardFace(Struct, tag_field="object", tag="card_face", kw_only=True):
    """A ScryCardFace represents a singl card face in a split, flip, transform, or meld card."""

    artist: str | None = None
    artist_id: UUID | None = None
    cmc: float | None = None
    color_indicator: list[ScryColor] | None = None
    colors: list[ScryColor] | None = None
    flavor_name: str | None = None
    flavor_text: str | None = None
    illustration_id: UUID | None = None
    image_uris: dict[str, str] | None = None
    layout: ScryCardLayout | None = None
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


class ScryCardPreviewBlock(Struct):
    """ScryCardPreviewBlock adds structure to ScryCard `preview` fields."""

    source: str
    source_uri: str
    previewed_at: dt.date


class ScryCard(
    Struct, tag_field="object", tag="card", kw_only=True, rename={"id_": "id", "set_": "set"}
):
    """ScryCard objects represent individual Magic: The Gathering cards."""

    # Core Card Fields
    arena_id: int | None = None
    id_: UUID
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
    all_parts: list[ScryRelatedCard] | None = None
    card_faces: list[ScryCardFace] | None = None
    cmc: float | None = None
    colors: list[ScryColor] | None = None
    color_identity: list[ScryColor]
    color_indicator: list[ScryColor] | None = None
    edhrec_rank: int | None = None
    foil: bool
    hand_modifier: str | None = None
    keywords: list[str]
    layout: ScryCardLayout
    legalities: dict[str, ScryCardLegality]
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
    border_color: ScryCardBorderColor
    card_back_id: UUID | None = None
    collector_number: str
    content_warning: bool | None = None
    digital: bool
    finishes: list[ScryCardFinish]
    flavor_name: str | None = None
    flavor_text: str | None = None
    frame_effect: ScryCardFrameEffect | None = None
    frame_effects: list[ScryCardFrameEffect] | None = None
    frame: ScryCardFrame
    full_art: bool
    games: list[ScryGame]
    highres_image: bool
    illustration_id: UUID | None = None
    image_status: ScryCardImageStatus
    image_uris: dict[str, str] | None = None
    prices: dict[str, Decimal | None] | None
    printed_name: str | None = None
    printed_text: str | None = None
    printed_type_line: str | None = None
    promo: bool
    promo_types: list[str] | None = None
    purchase_uris: dict[str, str] | None = None
    rarity: ScryCardRarity
    related_uris: dict[str, str] | None = None
    released_at: dt.date
    reprint: bool
    scryfall_set_uri: str
    set_name: str
    set_search_uri: str
    set_type: str
    set_uri: str
    set_: str
    set_id: UUID
    story_spotlight: bool
    textless: bool
    variation: bool
    variation_of: UUID | None = None
    security_stamp: ScryCardSecurityStamp | None = None
    watermark: str | None = None
    preview: ScryCardPreviewBlock | None = None

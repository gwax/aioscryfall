"""Scryfall API client methods for Card Objects.

Documentation: https://scryfall.com/docs/api/cards
"""

from enum import Enum
from typing import TYPE_CHECKING, TypeAlias, TypedDict, overload
from uuid import UUID

import msgspec.json

from aioscryfall.models.cards import ScryCard
from aioscryfall.models.catalogs import ScryCatalog
from aioscryfall.models.lists import ScryList

from . import responses

if TYPE_CHECKING:
    from aiohttp import ClientSession


class UniqueMode(Enum):
    """Unique mode for card search."""

    CARDS = "cards"  # default
    ART = "art"
    PRINTS = "prints"


class SortOrdering(Enum):
    """Sort ordering for card search."""

    NAME = "name"
    SET = "set"
    RELEASED = "released"
    RARITY = "rarity"
    COLOR = "color"
    USD = "usd"
    TIX = "tix"
    EUR = "eur"
    CMC = "cmc"
    POWER = "power"
    TOUGHNESS = "toughness"
    EDHREC = "edhrec"
    PENNY = "penny"
    ARTIST = "artist"
    REVIEW = "review"


class SortDirection(Enum):
    """Sort direction for card search."""

    AUTO = "auto"  # default
    ASC = "asc"
    DESC = "desc"


async def search(
    session: "ClientSession",
    query: str,
    *,
    unique: UniqueMode | None = None,
    order: SortOrdering | None = None,
    direction: SortDirection | None = None,
    include_extras: bool | None = None,
    include_multilingual: bool | None = None,
    include_variations: bool | None = None,
    page: int | None = None,
) -> ScryList[ScryCard]:
    """Client implementation for the Scryfall API's /cards/search endpoint.

    Documentation: https://scryfall.com/docs/api/cards/search
    """
    url = "https://api.scryfall.com/cards/search"
    params = {"q": query}
    if unique is not None:
        params["unique"] = unique.value
    if order is not None:
        params["order"] = order.value
    if direction is not None:
        params["dir"] = direction.value
    if include_extras is not None:
        params["include_extras"] = "true" if include_extras else "false"
    if include_multilingual is not None:
        params["include_multilingual"] = "true" if include_multilingual else "false"
    if include_variations is not None:
        params["include_variations"] = "true" if include_variations else "false"
    if page is not None:
        params["page"] = str(page)

    async with session.get(url, params=params) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryCard])


@overload
async def named(
    session: "ClientSession",
    *,
    exact: str,
    set_code: str | None = None,
) -> ScryCard:
    ...


@overload
async def named(
    session: "ClientSession",
    *,
    fuzzy: str,
    set_code: str | None = None,
) -> ScryCard:
    ...


async def named(
    session: "ClientSession",
    *,
    exact: str | None = None,
    fuzzy: str | None = None,
    set_code: str | None = None,
) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/named endpoint.

    Documentation: https://scryfall.com/docs/api/cards/named
    """
    if (exact is None and fuzzy is None) or (exact is not None and fuzzy is not None):
        msg = "Must specify one and only one of exact or fuzzy"
        raise ValueError(msg)

    url = "https://api.scryfall.com/cards/named"
    params = {}
    if exact is not None:
        params["exact"] = exact
    if fuzzy is not None:
        params["fuzzy"] = fuzzy
    if set_code is not None:
        params["set"] = set_code

    async with session.get(url, params=params) as resp:
        return await responses.read_response_payload(resp, ScryCard)


async def autocomplete(
    session: "ClientSession", query: str, *, include_extras: bool | None = None
) -> ScryCatalog:
    """Client implementation for the Scryfall API's /cards/autocomplete endpoint.

    Documentation: https://scryfall.com/docs/api/cards/autocomplete
    """
    url = "https://api.scryfall.com/cards/autocomplete"
    params = {"q": query}
    if include_extras is not None:
        params["include_extras"] = "true" if include_extras else "false"

    async with session.get(url, params=params) as resp:
        return await responses.read_response_payload(resp, ScryCatalog)


async def random(session: "ClientSession", *, query: str | None = None) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/random endpoint.

    Documentation: https://scryfall.com/docs/api/cards/random
    """
    url = "https://api.scryfall.com/cards/random"
    params = {}
    if query is not None:
        params["q"] = query

    async with session.get(url, params=params) as resp:
        return await responses.read_response_payload(resp, ScryCard)


class IdCardIdentifier(TypedDict):
    """Type definition for a card identifier by ID."""

    id: UUID  # noqa: A003


class MtgoIdCardIdentifier(TypedDict):
    """Type definition for a card identifier by MTGO ID."""

    mtgo_id: int


class MultiverseIdCardIdentifier(TypedDict):
    """Type definition for a card identifier by Multiverse ID."""

    multiverse_id: int


class OracleIdCardIdentifier(TypedDict):
    """Type definition for a card identifier by Oracle ID."""

    oracle_id: UUID


class IllustrationIdCardIdentifier(TypedDict):
    """Type definition for a card identifier by illustration ID."""

    illustration_id: UUID


class NameCardIdentifier(TypedDict):
    """Type definition for a card identifier by name."""

    name: str


class NameSetCardIdentifier(TypedDict):
    """Type definition for a card identifier by name and set."""

    name: str
    set: str  # noqa: A003


class CollectorNumberSetCardIdentifier(TypedDict):
    """Type definition for a card identifier by collector number and set."""

    collector_number: str
    set: str  # noqa: A003


CardIdentifier: TypeAlias = (
    IdCardIdentifier
    | MtgoIdCardIdentifier
    | MultiverseIdCardIdentifier
    | OracleIdCardIdentifier
    | IllustrationIdCardIdentifier
    | NameCardIdentifier
    | NameSetCardIdentifier
    | CollectorNumberSetCardIdentifier
)


async def collection(
    session: "ClientSession", identifiers: list[CardIdentifier]
) -> ScryList[ScryCard]:
    """Client implementation for the Scryfall API's /cards/collection endpoint.

    Documentation: https://scryfall.com/docs/api/cards/collection
    """
    url = "https://api.scryfall.com/cards/collection"
    headers = {"Content-Type": "application/json"}
    body = {"identifiers": identifiers}
    data = msgspec.json.encode(body)
    async with session.post(url, headers=headers, data=data) as resp:
        return await responses.read_response_payload(resp, ScryList[ScryCard])


async def getby_set_code_and_number(
    session: "ClientSession",
    set_code: str,
    collector_number: str,
    *,
    lang: str | None = None,
) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/:code/:number(/:lang) endpoint.

    Documentation: https://scryfall.com/docs/api/cards/collector
    """
    url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}"
    if lang is not None:
        url += f"/{lang}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryCard)


async def getby_multiverse_id(session: "ClientSession", multiverse_id: int) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/multiverse/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/multiverse
    """
    url = f"https://api.scryfall.com/cards/multiverse/{multiverse_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryCard)


async def getby_mtgo_id(session: "ClientSession", mtgo_id: int) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/mtgo/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/mtgo
    """
    url = f"https://api.scryfall.com/cards/mtgo/{mtgo_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryCard)


async def getby_arena_id(session: "ClientSession", arena_id: int) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/arena/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/arena
    """
    url = f"https://api.scryfall.com/cards/arena/{arena_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryCard)


async def getby_tcgplayer_id(session: "ClientSession", tcgplayer_id: int) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/tcgplayer/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/tcgplayer
    """
    url = f"https://api.scryfall.com/cards/tcgplayer/{tcgplayer_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryCard)


async def getby_cardmarket_id(session: "ClientSession", cardmarket_id: int) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/cardmarket/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/cardmarket
    """
    url = f"https://api.scryfall.com/cards/cardmarket/{cardmarket_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryCard)


async def getby_id(session: "ClientSession", scryfall_id: UUID) -> ScryCard:
    """Client implementation for the Scryfall API's /cards/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/get
    """
    url = f"https://api.scryfall.com/cards/{scryfall_id}"
    async with session.get(url) as resp:
        return await responses.read_response_payload(resp, ScryCard)

"""Scryfall API client methods for Card Objects.

Documentation: https://scryfall.com/docs/api/cards
"""

from enum import Enum
from typing import TYPE_CHECKING, TypeAlias, TypedDict, overload
from uuid import UUID

import msgspec.json

from . import responses
from .models import Card, Catalog, List

if TYPE_CHECKING:
    from aiohttp import ClientSession


class UniqueMode(Enum):
    CARDS = "cards"  # default
    ART = "art"
    PRINTS = "prints"


class SortOrdering(Enum):
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
) -> List[Card]:
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
        return await responses.parse(resp, List[Card])


@overload
async def named(
    session: "ClientSession",
    *,
    exact: str,
    set_code: str | None = None,
) -> Card:
    ...


@overload
async def named(
    session: "ClientSession",
    *,
    fuzzy: str,
    set_code: str | None = None,
) -> Card:
    ...


async def named(
    session: "ClientSession",
    *,
    exact: str | None = None,
    fuzzy: str | None = None,
    set_code: str | None = None,
) -> Card:
    """Client implementation for the Scryfall API's /cards/named endpoint.

    Documentation: https://scryfall.com/docs/api/cards/named
    """
    if exact is None and fuzzy is None:
        raise ValueError("Must specify one of exact or fuzzy")

    url = "https://api.scryfall.com/cards/named"
    params = {}
    if exact is not None:
        params["exact"] = exact
    if fuzzy is not None:
        params["fuzzy"] = fuzzy
    if set_code is not None:
        params["set"] = set_code

    async with session.get(url, params=params) as resp:
        return await responses.parse(resp, Card)


async def autocomplete(
    session: "ClientSession", query: str, *, include_extras: bool | None = None
) -> Catalog:
    """Client implementation for the Scryfall API's /cards/autocomplete endpoint.

    Documentation: https://scryfall.com/docs/api/cards/autocomplete
    """
    url = "https://api.scryfall.com/cards/autocomplete"
    params = {"q": query}
    if include_extras is not None:
        params["include_extras"] = "true" if include_extras else "false"

    async with session.get(url, params=params) as resp:
        return await responses.parse(resp, Catalog)


async def random(session: "ClientSession", *, query: str | None = None) -> Card:
    """Client implementation for the Scryfall API's /cards/random endpoint.

    Documentation: https://scryfall.com/docs/api/cards/random
    """
    url = "https://api.scryfall.com/cards/random"
    params = {}
    if query is not None:
        params["q"] = query

    async with session.get(url, params=params) as resp:
        return await responses.parse(resp, Card)


class IdCardIdentifier(TypedDict):
    id: UUID


class MtgoIdCardIdentifier(TypedDict):
    mtgo_id: int


class MultiverseIdCardIdentifier(TypedDict):
    multiverse_id: int


class OracleIdCardIdentifier(TypedDict):
    oracle_id: UUID


class IllustrationIdCardIdentifier(TypedDict):
    illustration_id: UUID


class NameCardIdentifier(TypedDict):
    name: str


class NameSetCardIdentifier(TypedDict):
    name: str
    set: str


class CollectorNumberSetCardIdentifier(TypedDict):
    collector_number: str
    set: str


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


async def collection(session: "ClientSession", identifiers: list[CardIdentifier]) -> List[Card]:
    """Client implementation for the Scryfall API's /cards/collection endpoint.

    Documentation: https://scryfall.com/docs/api/cards/collection
    """
    url = "https://api.scryfall.com/cards/collection"
    headers = {"Content-Type": "application/json"}
    body = {"identifiers": identifiers}
    data = msgspec.json.encode(body)
    print(body, msgspec.json.encode(body))
    async with session.post(url, headers=headers, data=data) as resp:
        return await responses.parse(resp, List[Card])


async def set_code_and_number(
    session: "ClientSession",
    set_code: str,
    collector_number: str,
    *,
    lang: str | None = None,
) -> Card:
    """Client implementation for the Scryfall API's /cards/:code/:number(/:lang) endpoint.

    Documentation: https://scryfall.com/docs/api/cards/collector
    """
    url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}"
    if lang is not None:
        url += f"/{lang}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Card)


async def multiverse_id(session: "ClientSession", multiverse_id: int) -> Card:
    """Client implementation for the Scryfall API's /cards/multiverse/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/multiverse
    """
    url = f"https://api.scryfall.com/cards/multiverse/{multiverse_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Card)


async def mtgo_id(session: "ClientSession", mtgo_id: int) -> Card:
    """Client implementation for the Scryfall API's /cards/mtgo/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/mtgo
    """
    url = f"https://api.scryfall.com/cards/mtgo/{mtgo_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Card)


async def arena_id(session: "ClientSession", arena_id: int) -> Card:
    """Client implementation for the Scryfall API's /cards/arena/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/arena
    """
    url = f"https://api.scryfall.com/cards/arena/{arena_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Card)


async def tcgplayer_id(session: "ClientSession", tcgplayer_id: int) -> Card:
    """Client implementation for the Scryfall API's /cards/tcgplayer/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/tcgplayer
    """
    url = f"https://api.scryfall.com/cards/tcgplayer/{tcgplayer_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Card)


async def cardmarket_id(session: "ClientSession", cardmarket_id: int) -> Card:
    """Client implementation for the Scryfall API's /cards/cardmarket/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/cardmarket
    """
    url = f"https://api.scryfall.com/cards/cardmarket/{cardmarket_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Card)


async def get(session: "ClientSession", scryfall_id: UUID) -> Card:
    """Client implementation for the Scryfall API's /cards/:id endpoint.

    Documentation: https://scryfall.com/docs/api/cards/get
    """
    url = f"https://api.scryfall.com/cards/{scryfall_id}"
    async with session.get(url) as resp:
        return await responses.parse(resp, Card)

"""Serialization and deserialization methods for Scryfall models."""

import typing
from contextvars import ContextVar
from typing import TYPE_CHECKING, TypeVar

import msgspec

from .lists import RawScryList, ScryList

if TYPE_CHECKING:
    from msgspec.json import Decoder

DECODER_CACHE: ContextVar[dict[type, "Decoder"]] = ContextVar("DECODER_CACHE", default={})


def _get_decoder(type_: type) -> "Decoder":
    """Create or retrieve a cached msgspec JSON decoder for a given type."""
    cache = DECODER_CACHE.get()
    if type_ not in cache:
        cache = cache.copy()
        cache[type_] = msgspec.json.Decoder(type_)
        DECODER_CACHE.set(cache)
    return cache[type_]


_T = TypeVar("_T")


def decode_json(data: bytes, type_: type[_T]) -> _T:
    """Decode JSON data using msgspec with some custom code for handling Scryfall lists."""
    if typing.get_origin(type_) is ScryList:
        raw_list = _get_decoder(RawScryList).decode(data)
        # We know that type_ is a ScryList[T] here, so we can ignore the false positive type error
        return type_.from_raw(raw_list)  # type: ignore
    return _get_decoder(type_).decode(data)

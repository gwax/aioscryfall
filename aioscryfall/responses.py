import typing
from contextvars import ContextVar
from typing import TYPE_CHECKING, Type, TypeVar

import msgspec

from . import errors, models

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from msgspec.json import Decoder

DECODER_CACHE: ContextVar[dict[Type, "Decoder"]] = ContextVar(
    "DECODER_CACHE", default={}
)


def _get_decoder(type_: Type) -> "Decoder":
    cache = DECODER_CACHE.get()
    if type_ not in cache:
        cache = cache.copy()
        cache[type_] = msgspec.json.Decoder(type_)
        DECODER_CACHE.set(cache)
    return cache[type_]


T = TypeVar("T")


async def parse(response: "ClientResponse", type_: Type[T]) -> T:
    """Parse a response from the Scryfall API and handle errors."""
    data = await response.read()
    if response.status >= 400:
        decoder = _get_decoder(models.Error)
        try:
            error = decoder.decode(data)
        except (msgspec.DecodeError, msgspec.ValidationError):
            raise errors.UnparsedAPIError(response.status, data[:100]) from None
        raise errors.APIError(response.status, error)

    if typing.get_origin(type_) is models.List:
        raw_list = _get_decoder(models.RawList).decode(data)
        # We know that type_ is a List[T] here, so we can safely ignore the false error
        return type_.from_raw(raw_list)  # type: ignore

    return _get_decoder(type_).decode(data)

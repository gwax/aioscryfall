"""Scryfall API client response reading and error handling helpers."""

from typing import TYPE_CHECKING, TypeVar

import msgspec

from aioscryfall.errors import APIError, UnparsedAPIError
from aioscryfall.models import serde
from aioscryfall.models.errors import ScryError

if TYPE_CHECKING:
    from aiohttp import ClientResponse


_T = TypeVar("_T")


async def read_response_payload(response: "ClientResponse", type_: type[_T]) -> _T:
    """Parse a successful response from the Scryfall API or raise an appropriate exceptoin."""
    data = await response.read()
    if response.status >= 400:  # noqa: PLR2004 - 400 is hardly a magic number
        try:
            scry_error = serde.decode_json(data, ScryError)
        except (msgspec.DecodeError, msgspec.ValidationError) as exc:
            raise UnparsedAPIError(response.status, data[:100]) from exc
        raise APIError(response.status, scry_error)
    return serde.decode_json(data, type_)

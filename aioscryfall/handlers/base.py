"""Base class for all handlers."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aioscryfall.client import ScryfallClient


class BaseHandler:
    """Base class for all handlers."""

    def __init__(self, client: "ScryfallClient") -> None:
        self._client = client

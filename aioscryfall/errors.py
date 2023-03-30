"""Exceptions for the aioscryfall package."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aioscryfall.models.errors import ScryError


class Error(Exception):
    """Base class for exceptions in this module."""


class UnparsedAPIError(Error):
    """Exception raised when the Scryfall API returns an unparsable error.

    Attributes
    ----------
        status_code: HTTP status code returned by the API.
        details: The error details returned by the API.
    """

    def __init__(self, status: int, details: bytes):
        super().__init__(f"Scryfall API returned unparsable error: {details!r}")
        self.status = status
        self.details = details


class APIError(Error):
    """Exception raised for errors from the Scryfall API.

    Attributes
    ----------
        status_code: HTTP status code returned by the API.
        error: The error object returned by the API.
    """

    def __init__(self, status: int, error: "ScryError"):
        super().__init__(f"Scryfall API returned error({status}): {error.details}")
        self.status = status
        self.error = error

"""Test utility functions."""

from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from aioresponses import aioresponses

TEST_DATA_DIR = Path(__file__).parent / "data"


async def load_get_payload(
    mock_aioresponses: "aioresponses", url: str, filename: str, *, status_code: int = 200
) -> None:
    """Load a mock payload from a file."""
    async with aiofiles.open(TEST_DATA_DIR / filename, "rb") as file:
        mock_aioresponses.get(url, status=status_code, body=await file.read())


def sync_load_get_payload(
    mock_aioresponses: "aioresponses", url: str, filename: str, *, status_code: int = 200
) -> None:
    """Load a mock payload from a file."""
    with open(TEST_DATA_DIR / filename, "rb") as file:
        mock_aioresponses.get(url, status=status_code, body=file.read())


async def load_post_payload(
    mock_aioresponses: "aioresponses",
    url: str,
    filename: str,
    *,
    status_code: int = 200,
) -> None:
    """Load a mock payload from a file."""
    async with aiofiles.open(TEST_DATA_DIR / filename, "rb") as file:
        mock_aioresponses.post(url, status=status_code, body=await file.read())


def sync_load_post_payload(
    mock_aioresponses: "aioresponses",
    url: str,
    filename: str,
    *,
    status_code: int = 200,
) -> None:
    """Load a mock payload from a file."""
    with open(TEST_DATA_DIR / filename, "rb") as file:
        mock_aioresponses.post(url, status=status_code, body=file.read())

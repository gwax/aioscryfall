"""Test utility functions."""

from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from aioresponses import aioresponses

TEST_DATA_DIR = Path(__file__).parent / "data"


async def load_get_payload(mock_aioresponses: "aioresponses", url: str, filename: str) -> None:
    """Load a mock payload from a file."""
    async with aiofiles.open(TEST_DATA_DIR / filename, "rb") as file:
        mock_aioresponses.get(url, body=await file.read())

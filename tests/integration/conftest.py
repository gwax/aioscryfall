from typing import AsyncGenerator

import pytest_asyncio
from aiohttp import ClientSession


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[ClientSession, None]:
    """Test session scoped aiohttp ClientSession."""
    async with ClientSession() as sess:
        yield sess

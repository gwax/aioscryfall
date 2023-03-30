"""Pytest configuration for integration tests."""

import asyncio
from typing import TYPE_CHECKING

import pytest
import pytest_asyncio
from aiohttp import ClientSession

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from collections.abc import AsyncGenerator, Generator


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark all tests in this folder as integration tests."""
    for item in items:
        item.add_marker("integration")


@pytest.fixture(scope="session")
def event_loop() -> "Generator[AbstractEventLoop, None, None]":
    """Test session scoped event loop."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client_session() -> "AsyncGenerator[ClientSession, None]":
    """Test session scoped aiohttp ClientSession."""
    async with ClientSession() as sess:
        yield sess

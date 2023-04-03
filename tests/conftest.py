"""Pytest configuration for aioscryfall tests."""

import asyncio
from typing import TYPE_CHECKING

import aioresponses
import pytest
import pytest_asyncio
from aiohttp import ClientSession

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from collections.abc import AsyncGenerator, Generator

    from _pytest.fixtures import FixtureRequest


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


@pytest.fixture(autouse=True)
def mock_aioresponse(
    request: "FixtureRequest",
) -> "Generator[aioresponses.aioresponses | None, None, None]":
    """Mock aiohttp responses."""
    marks = {m.name for m in request.node.iter_markers()}
    if request.node.parent:
        marks.update({m.name for m in request.node.parent.iter_markers()})
    if "integration" in marks:
        yield None
    else:
        with aioresponses.aioresponses() as mock:
            yield mock

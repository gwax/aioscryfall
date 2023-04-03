"""Pytest configuration for integration tests."""

from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from aiolimiter import AsyncLimiter

LIMITER = AsyncLimiter(10, 1)  # 10 requests per second


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark all tests in this folder as integration tests."""
    conftest_path = Path(__file__).parent
    for item in items:
        if conftest_path in Path(item.fspath).parents:
            item.add_marker("integration")


@pytest.fixture(autouse=True)
async def _limit_requests() -> AsyncGenerator[None, None]:
    """Limit requests to 10 per second."""
    async with LIMITER:
        yield

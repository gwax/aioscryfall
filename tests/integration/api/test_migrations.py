"""Integration tests for aioscryfall.api.migrations."""

from typing import TYPE_CHECKING
from uuid import UUID

from aioscryfall.api import migrations

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def test_all_migrations(client_session: "ClientSession") -> None:
    result = await migrations.all_migrations(client_session)
    assert result.data


async def test_get(client_session: "ClientSession") -> None:
    result = await migrations.getby_id(
        client_session, UUID("6697b38a-ee19-455c-b24b-d0a659782d8b")
    )
    assert result.note == "Un-rebalanced on Arena"

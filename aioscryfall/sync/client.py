"""Synchronous Scryfall client."""

import asyncio
import contextlib

import aiohttp

from aioscryfall.client import ScryfallClient
from aioscryfall.sync.handlers.bulk_data import BulkDataSyncHandler
from aioscryfall.sync.handlers.catalogs import CatalogsSyncHandler
from aioscryfall.sync.handlers.migrations import MigrationsSyncHandler
from aioscryfall.sync.handlers.rulings import RulingsSyncHandler
from aioscryfall.sync.handlers.symbols import SymbolsSyncHandler


class ScryfallSyncClient:
    """ScryfallSyncClient is a synchronous client for the Scryfall API."""

    def __init__(self) -> None:
        self._sessions: dict[asyncio.AbstractEventLoop, aiohttp.ClientSession] = {}
        self._async_clients: dict[asyncio.AbstractEventLoop, ScryfallClient] = {}

        # Mount handlers
        self.bulk_data = BulkDataSyncHandler(self)
        self.catalogs = CatalogsSyncHandler(self)
        self.migrations = MigrationsSyncHandler(self)
        self.rulings = RulingsSyncHandler(self)
        self.symbols = SymbolsSyncHandler(self)

    def get_event_loop(self) -> asyncio.AbstractEventLoop:
        """Get the event loop for the current thread."""
        loop = None
        with contextlib.suppress(RuntimeError):
            loop = asyncio.get_event_loop_policy().get_event_loop()
        if loop is None or loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    def get_async_client(self) -> ScryfallClient:
        """Get an async client for the current thread."""
        loop = self.get_event_loop()
        session = self._sessions.get(loop)
        if session is None or session.closed:
            session = aiohttp.ClientSession(loop=loop)
            self._sessions[loop] = session
        client = self._async_clients.get(loop)
        if client is None:
            client = ScryfallClient(session)
            self._async_clients[loop] = client
        return client

    def close(self) -> None:
        """Close the client, cleaning up the internal aiohttp session."""

        async def _close_sessions() -> None:
            for key, session in self._sessions.items():
                if key in self._async_clients:
                    del self._async_clients[key]
                if session is not None and not session.closed:
                    await session.close()

        loop = self.get_event_loop()
        if loop.is_running():
            loop.create_task(_close_sessions())
        else:
            loop.run_until_complete(_close_sessions())

    def __del__(self) -> None:
        """Ensure client is closed when it is garbage collected."""
        self.close()

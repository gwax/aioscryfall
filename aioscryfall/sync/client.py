"""Synchronous Scryfall client."""


from aioscryfall.sync.handlers.bulk_data import BulkDataSyncHandler
from aioscryfall.sync.handlers.symbols import SymbolsSyncHandler


class ScryfallSyncClient:
    """ScryfallSyncClient is a synchronous client for the Scryfall API."""

    def __init__(self) -> None:
        self.bulk_data = BulkDataSyncHandler()
        self.symbols = SymbolsSyncHandler()

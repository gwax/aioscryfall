"""Client handler for the Scryfall catalogs APIs."""

from aioscryfall.api import catalogs

from .base import BaseHandler


class CatalogsHandler(BaseHandler):
    """ScryfallClient handler for catalogs APIs."""

    async def card_names(self) -> list[str]:
        """Get a list of all card names."""
        async with self._client.limiter:
            catalog = await catalogs.card_names(self._client.session)
        return catalog.data

    async def artist_names(self) -> list[str]:
        """Get a list of all artist names."""
        async with self._client.limiter:
            catalog = await catalogs.artist_names(self._client.session)
        return catalog.data

    async def word_bank(self) -> list[str]:
        """Get a list of all words used in card text."""
        async with self._client.limiter:
            catalog = await catalogs.word_bank(self._client.session)
        return catalog.data

    async def creature_types(self) -> list[str]:
        """Get a list of all creature types."""
        async with self._client.limiter:
            catalog = await catalogs.creature_types(self._client.session)
        return catalog.data

    async def planeswalker_types(self) -> list[str]:
        """Get a list of all planeswalker types."""
        async with self._client.limiter:
            catalog = await catalogs.planeswalker_types(self._client.session)
        return catalog.data

    async def land_types(self) -> list[str]:
        """Get a list of all land types."""
        async with self._client.limiter:
            catalog = await catalogs.land_types(self._client.session)
        return catalog.data

    async def artifact_types(self) -> list[str]:
        """Get a list of all artifact types."""
        async with self._client.limiter:
            catalog = await catalogs.artifact_types(self._client.session)
        return catalog.data

    async def enchantment_types(self) -> list[str]:
        """Get a list of all enchantment types."""
        async with self._client.limiter:
            catalog = await catalogs.enchantment_types(self._client.session)
        return catalog.data

    async def spell_types(self) -> list[str]:
        """Get a list of all spell types."""
        async with self._client.limiter:
            catalog = await catalogs.spell_types(self._client.session)
        return catalog.data

    async def powers(self) -> list[str]:
        """Get a list of all power values."""
        async with self._client.limiter:
            catalog = await catalogs.powers(self._client.session)
        return catalog.data

    async def toughnesses(self) -> list[str]:
        """Get a list of all toughness values."""
        async with self._client.limiter:
            catalog = await catalogs.toughnesses(self._client.session)
        return catalog.data

    async def loyalties(self) -> list[str]:
        """Get a list of all loyalty values."""
        async with self._client.limiter:
            catalog = await catalogs.loyalties(self._client.session)
        return catalog.data

    async def watermarks(self) -> list[str]:
        """Get a list of all watermarks."""
        async with self._client.limiter:
            catalog = await catalogs.watermarks(self._client.session)
        return catalog.data

    async def keyword_abilities(self) -> list[str]:
        """Get a list of all keyword abilities."""
        async with self._client.limiter:
            catalog = await catalogs.keyword_abilities(self._client.session)
        return catalog.data

    async def keyword_actions(self) -> list[str]:
        """Get a list of all keyword actions."""
        async with self._client.limiter:
            catalog = await catalogs.keyword_actions(self._client.session)
        return catalog.data

    async def ability_words(self) -> list[str]:
        """Get a list of all ability words."""
        async with self._client.limiter:
            catalog = await catalogs.ability_words(self._client.session)
        return catalog.data

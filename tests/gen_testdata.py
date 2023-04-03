"""Script to build test data files for the test suite."""

from pathlib import Path
from typing import Any

import aiofiles.os
import msgspec
from aiohttp import ClientSession
from aiolimiter import AsyncLimiter

from aioscryfall.api import bulk_data, cards, catalogs, migrations, rulings, sets, symbols
from aioscryfall.models.lists import RawScryList, ScryList

TEST_DATA_DIR = Path(__file__).parent / "data"
ENCODER = msgspec.json.Encoder()
LIMITER = AsyncLimiter(10, 1)  # 10 requests per second


def _pretty_encode(obj: Any) -> bytes:
    """Encode an object to JSON with pretty formatting."""
    if isinstance(obj, ScryList):
        obj = RawScryList(
            data=obj.data,
            has_more=obj.has_more,
            next_page=obj.next_page,
            total_cards=obj.total_cards,
            warnings=obj.warnings,
        )
    return msgspec.json.format(ENCODER.encode(obj))


async def update_bulk_data(session: "ClientSession") -> None:
    """Update the bulk data test data files."""
    bulk_data_path = TEST_DATA_DIR / "bulk_data"
    await aiofiles.os.makedirs(bulk_data_path, exist_ok=True)

    async with LIMITER:
        all_bulk_data = await bulk_data.all_bulk_data(session)

    async with aiofiles.open(bulk_data_path / "all.json", "wb") as file:
        await file.write(_pretty_encode(all_bulk_data))

    async with aiofiles.open(bulk_data_path / "single.json", "wb") as file:
        await file.write(_pretty_encode(all_bulk_data.data[0]))


async def update_cards(session: "ClientSession") -> None:
    """Update the cards test data files."""
    cards_path = TEST_DATA_DIR / "cards"
    await aiofiles.os.makedirs(cards_path, exist_ok=True)

    async with LIMITER:
        forests = await cards.search(session, "t:land t:forest", unique=cards.UniqueMode.PRINTS)

    forests_page1 = ScryList(
        data=forests.data[:10],
        has_more=True,
        next_page="https://api.scryfall.com/cards/search?some_args=stuff",
        total_cards=20,
    )
    forests_page2 = ScryList(data=forests.data[10:20], has_more=False, total_cards=20)
    async with aiofiles.open(cards_path / "forests-page1.json", "wb") as file:
        await file.write(_pretty_encode(forests_page1))
    async with aiofiles.open(cards_path / "forests-page2.json", "wb") as file:
        await file.write(_pretty_encode(forests_page2))

    async with LIMITER:
        async with aiofiles.open(cards_path / "single.json", "wb") as file:
            await file.write(
                _pretty_encode(await cards.getby_set_code_and_number(session, "mh2", "259"))
            )

    async with LIMITER:
        async with aiofiles.open(cards_path / "autocomplete.json", "wb") as file:
            await file.write(_pretty_encode(await cards.autocomplete(session, "snow-covered")))


async def updata_catalogs(session: "ClientSession") -> None:
    """Update the catalogs test data files."""
    catalog_path = TEST_DATA_DIR / "catalog"
    await aiofiles.os.makedirs(catalog_path, exist_ok=True)

    for filename, func in (
        ("card-names.json", catalogs.card_names),
        ("artist-names.json", catalogs.artist_names),
        ("word-bank.json", catalogs.word_bank),
        ("creature-types.json", catalogs.creature_types),
        ("planeswalker-types.json", catalogs.planeswalker_types),
        ("land-types.json", catalogs.land_types),
        ("artifact-types.json", catalogs.artifact_types),
        ("enchantment-types.json", catalogs.enchantment_types),
        ("spell-types.json", catalogs.spell_types),
        ("powers.json", catalogs.powers),
        ("toughnesses.json", catalogs.toughnesses),
        ("loyalties.json", catalogs.loyalties),
        ("watermarks.json", catalogs.watermarks),
        ("keyword-abilities.json", catalogs.keyword_abilities),
        ("keyword-actions.json", catalogs.keyword_actions),
        ("ability-words.json", catalogs.ability_words),
    ):
        async with LIMITER:
            async with aiofiles.open(catalog_path / filename, "wb") as file:
                await file.write(_pretty_encode(await func(session)))


async def update_migrations(session: "ClientSession") -> None:
    """Update the migrations test data files."""
    migrations_path = TEST_DATA_DIR / "migrations"
    await aiofiles.os.makedirs(migrations_path, exist_ok=True)

    async with LIMITER:
        all_migrations = await migrations.all_migrations(session)

    async with aiofiles.open(migrations_path / "single.json", "wb") as file:
        await file.write(_pretty_encode(all_migrations.data[0]))

    page1 = ScryList(
        data=all_migrations.data[:10],
        has_more=True,
        next_page="https://api.scryfall.com/migrations?page=2",
    )
    page2 = ScryList(data=all_migrations.data[10:20], has_more=False)
    async with aiofiles.open(migrations_path / "page1.json", "wb") as file:
        await file.write(_pretty_encode(page1))
    async with aiofiles.open(migrations_path / "page2.json", "wb") as file:
        await file.write(_pretty_encode(page2))


async def update_rulings(session: "ClientSession") -> None:
    """Update the rulings test data files."""
    rulings_path = TEST_DATA_DIR / "rulings"
    await aiofiles.os.makedirs(rulings_path, exist_ok=True)

    async with LIMITER:
        async with aiofiles.open(rulings_path / "single.json", "wb") as file:
            await file.write(
                _pretty_encode(await rulings.getby_set_code_and_number(session, "rtr", "213"))
            )


async def update_sets(session: "ClientSession") -> None:
    """Update the sets test data files."""
    sets_path = TEST_DATA_DIR / "sets"
    await aiofiles.os.makedirs(sets_path, exist_ok=True)

    async with LIMITER:
        all_sets = await sets.all_sets(session)

    async with aiofiles.open(sets_path / "single.json", "wb") as file:
        await file.write(_pretty_encode(all_sets.data[0]))

    page1 = ScryList(
        data=all_sets.data[:10],
        has_more=True,
        next_page="https://api.scryfall.com/sets?page=2",
    )
    page2 = ScryList(data=all_sets.data[10:20], has_more=False)
    async with aiofiles.open(sets_path / "page1.json", "wb") as file:
        await file.write(_pretty_encode(page1))
    async with aiofiles.open(sets_path / "page2.json", "wb") as file:
        await file.write(_pretty_encode(page2))


async def update_symbols(session: "ClientSession") -> None:
    """Update the symbols test data files."""
    symbols_path = TEST_DATA_DIR / "symbols"
    await aiofiles.os.makedirs(symbols_path, exist_ok=True)

    async with LIMITER:
        all_card_symbols = await symbols.all_card_symbols(session)

    page1 = ScryList(
        data=all_card_symbols.data[:10],
        has_more=True,
        next_page="https://api.scryfall.com/symbols?page=2",
    )
    page2 = ScryList(data=all_card_symbols.data[10:20], has_more=False)
    async with aiofiles.open(symbols_path / "card-symbols-page1.json", "wb") as file:
        await file.write(_pretty_encode(page1))
    async with aiofiles.open(symbols_path / "card-symbols-page2.json", "wb") as file:
        await file.write(_pretty_encode(page2))

    async with LIMITER:
        async with aiofiles.open(symbols_path / "parse-mana-single.json", "wb") as file:
            await file.write(_pretty_encode(await symbols.parse_mana(session, "BUGX")))


async def main() -> None:
    """Run the script."""
    await aiofiles.os.makedirs(TEST_DATA_DIR, exist_ok=True)
    async with ClientSession() as session:
        await update_bulk_data(session)
        await update_cards(session)
        await updata_catalogs(session)
        await update_migrations(session)
        await update_rulings(session)
        await update_sets(session)
        await update_symbols(session)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

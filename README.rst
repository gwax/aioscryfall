aioscryfall - Asynchronous Python client for Scryfall API
=========================================================

This is an early work in progress. I am currently in the phase of getting all of the
features in place. Once everything is in place, I will clean up the API and add
some abstraction layers and documentation on top.

For now, the API is very low level and you will need to read the Scryfall API and
the code to figure out how to use it.

You will need Python >= 3.11 (I may change this to support earlier versions in the future) and you will need to use aiohttp.

A minimal use case to get yourself started:

.. code:: python

    import asyncio
    import aiohttp
    from aioscryfall.api.cards import UniqueMode
    import aioscryfall.client import ScryfallClient

    async def get_bolt():
        async with aiohttp.ClientSession() as session:
            client = ScryfallClient(session)
            bolts = [c async for c in client.cards.search("lightning bolt", unique=UniqueMode.PRINTS)]
            return bolts

    bolts = asyncio.run(get_bolt())
    print(len(bolts), bolts[0])

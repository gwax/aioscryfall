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
    import aioscryfall.cards

    async def get_bolt():
        async with aiohttp.ClientSession() as session:
            card_list = await aioscryfall.cards.search(session, "lightning bolt")
            return card_list.data[0]

    bolt = asyncio.run(get_bolt())
    print(bolt)

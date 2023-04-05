aioscryfall - Asynchronous Python client for Scryfall API
=========================================================

aioscryfall is a Python client for the Scryfall API. It is primarily designed for asynchronous use with asyncio, but a synchronous client is also provided.

The development is essentially feature complete but the documentation is largely absent, at present. (I need to remind myself how mkdocs works and figure out what I want to say)

As of right now, Python 3.11 is required because I wanted to use a number of typing features that were added in 3.11. I may change this in the future, but it is a lower priority than getting the API to a point where I am happy with it.

Everything is extensively typed and I have tried to make the API as intuitive as possible. I have also tried to make the API as close to the Scryfall API as possible, but I have made some changes to make it more Pythonic (namely converting paginated lists into iterable generators).

A minimal use case to get yourself started:

.. code:: python

    import asyncio
    import aiohttp
    from aioscryfall.api.cards import UniqueMode
    from aioscryfall.client import ScryfallClient

    async def get_bolt():
        async with aiohttp.ClientSession() as session:
            client = ScryfallClient(session)
            bolts = [c async for c in client.cards.search("lightning bolt", unique=UniqueMode.PRINTS)]
            return bolts

    bolts = asyncio.run(get_bolt())
    print(len(bolts), bolts[0])

Or if you prefer not to use async:

.. code:: python

    from aioscryfall.api.cards import UniqueMode
    from aioscryfall.sync.client import ScryfallSyncClient

    client = ScryfallSyncClient()
    bolts = list(client.cards.search("lightning bolt", unique=UniqueMode.PRINTS))
    print(len(bolts), bolts[0])

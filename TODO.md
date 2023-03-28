# TODO

-   Properly setup linters and test runners
-   Add a client class to abstract out the aiohttp ClientSession creation
-   Add a token pool to enforce 10 request per second limit
-   Use aiohttp for fetching bulk data objects
-   Add a synchronous client for folks that want one
-   Split up the models file and reorganize the low level client calls
-   Documentation
-   Do we want to support older versions of Python? It would be friendly but it makes the type annotations uglier...

# Package layout thoughts

```
aioscryfall
├── api
│   ├── bulk_data.py
│   ├── cards.py
│   ├── etc... (low level api functions)
|
├── models
|   ├── cards.py
│   ├── enums.py
│   ├── errors.py
│   ├── etc... (data models)
│
├── client (async client)
│
├── sync_client (sync client)
```

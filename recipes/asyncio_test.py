#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Experiment using the Python3 asyncio module.

Futher information can be found at
https://docs.python.org/3.5/library/asyncio.html
https://www.python.org/dev/peps/pep-0492/
"""

import asyncio  # Base library for python's asynchronous I/O submodule

import aiohttp  # An async-io enabled HTTP submodule

# Something to fetch
urls = [
    'https://twitter.com/basti_tee'
]

# create a basic node.js-like event loop
event_loop = asyncio.get_event_loop()
# create a new HTTP session with aio-capabilities
session = aiohttp.ClientSession(loop=event_loop)


async def fetch(session, url):
    """Async function to fetch a single URL using the aio-http session."""
    # The async keyword makes the function a coroutine
    async with session.get(url) as response:
        # Await suspends a coroutine on an awaitable object
        return await response.read()


async def fetch_all(session, urls, event_loop):
    """Async function to fetch multiple URLs using the aio-http session."""
    # Create a list of future objects for each given URL
    futures = [fetch(session, url) for url in urls]
    # Return a future aggregating results from the given futures
    return await asyncio.gather(*futures)

# create a future object to be executed on our event loop.
# https://docs.python.org/3/library/asyncio-task.html#asyncio.Future
future = fetch_all(session, urls, event_loop)
# invoke event loop process by running this blocking call which returns
# when all coroutines (indicated by async keyword) are done
responses = event_loop.run_until_complete(future)

# explicit closing. we could avoid this using 'with' blocks
session.close()

# result processing
print(f'fetched {len(responses)} responses.')

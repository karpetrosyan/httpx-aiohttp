# Introduction

<p align="center">
<i>httpx-aiohttp</i> - provides transports for <a href="https://www.python-httpx.org/"><i>httpx</i></a> to work on top of <a href="https://docs.aiohttp.org/en/stable/client.html"><i>aiohttp</i></a>, handling all high-level features like authentication, retries, and cookies through httpx, while delegating low-level socket-level HTTP messaging to <i>aiohttp</i>
</p>

## via HttpxAiohttpClient

The `HttpxAiohttpClient` class is an alternative to the `AsyncClient` class that changes the underlying transport from the default `AsyncHTTPTransport` to `AiohttpTransport`.

```py
import asyncio
from httpx_aiohttp import HttpxAiohttpClient


async def main() -> None:
    async with HttpxAiohttpClient() as client:
        response = await client.get("https://encode.io")
        print(response)

asyncio.run(main())
```

## via AiohttpTransport

You can also change the transport itself by passing the transport object to the default `AsyncClient`, asking it to use that particular transport.

```py
import httpx
import asyncio
from httpx_aiohttp import AiohttpTransport


async def main() -> None:
    async with httpx.AsyncClient(transport=AiohttpTransport()) as client:
        response = await client.get("https://encode.io.com")
        print(response)


asyncio.run(main())
```

!!! note "Choose your option carefully"
    If you aren't familiar with how the client operates with transports, it's preferable to replace the client with the one that httpx_aiohttp provides. Providing a transport forces the client to use that transport by default or for some particular URL pattern, so some client arguments won't work (for example, client timeout configurations won't be respected when you provide your own transport).

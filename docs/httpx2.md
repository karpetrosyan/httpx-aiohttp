# httpx2 support

[httpx2](https://github.com/pydantic/httpx2) is an API-compatible continuation of httpx maintained by the Pydantic team. httpx-aiohttp ships a variant of its client and transport built against httpx2 instead of httpx.

httpx2 support is optional. Install it with the `httpx2` extra:

```shell
uv pip install httpx-aiohttp[httpx2]
```

## via Httpx2AiohttpClient

`Httpx2AiohttpClient` is the httpx2 counterpart of `HttpxAiohttpClient`: an alternative to `httpx2.AsyncClient` that uses aiohttp as the underlying transport.

```py
import asyncio
from httpx_aiohttp.httpx2 import Httpx2AiohttpClient


async def main() -> None:
    async with Httpx2AiohttpClient() as client:
        response = await client.get("https://encode.io")
        print(response)

asyncio.run(main())
```

## via AiohttpTransport

The `httpx_aiohttp.httpx2` module also exposes an `AiohttpTransport` that implements `httpx2.AsyncBaseTransport`, so you can plug it into a plain `httpx2.AsyncClient`:

```py
import asyncio
import httpx2
from httpx_aiohttp.httpx2 import AiohttpTransport


async def main() -> None:
    async with httpx2.AsyncClient(transport=AiohttpTransport()) as client:
        response = await client.get("https://encode.io")
        print(response)


asyncio.run(main())
```

Everything on the [compatibility page](compatibility.md) applies to the httpx2 variant as well — exceptions are raised as `httpx2` exception types (e.g. `httpx2.ConnectError`) instead of `httpx` ones.

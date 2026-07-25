# Compatibility

You may encounter some differences when working with alternative transports. This page describes the differences between the default transport and the aiohttp-powered one.

## Timeouts

Timeouts will work for the aiohttp-powered transport, except for the write timeout, which isn't currently supported in aiohttp.

```python
import asyncio
from httpx_aiohttp import HttpxAiohttpClient


async def main() -> None:
    async with HttpxAiohttpClient() as client:
        response = await httpx_client.get("https://www.encode.io", timeout=httpx.Timeout(
            connect=5.0,
            read=5.0,
            pool=5.0,
            write=None  # Aiohttp doesn't support write timeout
        ))
        print(response)

asyncio.run(main())
```

## Proxies

HTTP proxies will work as expected, though aiohttp doesn't have built-in support for SOCKS and HTTPS proxies like httpx does. If you want to use SOCKS proxies, for example, you can inject a third-party SOCKS implementation client session (such as [aiohttp-socks](https://pypi.org/project/aiohttp-socks/)) into the httpx client.

```python
import asyncio
from httpx_aiohttp import HttpxAiohttpClient

async def main() -> None:
    async with HttpxAiohttpClient(
        proxy="http://127.0.0.1:9001",  # you can use mitmproxy
    ) as client:
        response = await client.get("http://www.encode.io")
        print(response)


asyncio.run(main())
```

## Event hooks

Event hooks will not work for the aiohttp-powered transport because hooks are called from httpcore, and aiohttp doesn't support them.

## Extensions

Extensions [trace](https://www.python-httpx.org/advanced/extensions/#trace), [target](https://www.python-httpx.org/advanced/extensions/#target), [stream_id](https://www.python-httpx.org/advanced/extensions/#stream_id) and [network_stream](https://www.python-httpx.org/advanced/extensions/#network_stream) are also not supported.

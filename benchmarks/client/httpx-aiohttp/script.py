# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx>=0.28.1",
#     "httpx-aiohttp",
#     "aiohttp",
# ]
# ///
import json
import os
import time

import aiohttp
import httpx
import asyncio
import httpx_aiohttp

SERVER_URL = os.getenv("SERVER_URL")
REQUESTS_COUNT = int(os.getenv("REQUESTS_COUNT"))

if SERVER_URL is None:
    raise RuntimeError("SERVER_URL environment variable is not set")


async def main() -> None:
    async with httpx_aiohttp.AiohttpTransport(
        client=aiohttp.ClientSession()
    ) as transport:
        async with httpx.AsyncClient(transport=transport) as client:
            tasks = []
            for _ in range(REQUESTS_COUNT):
                tasks.append(asyncio.create_task(client.get(SERVER_URL)))
            t1 = time.monotonic()
            results = await asyncio.gather(*tasks)
            t2 = time.monotonic()

    with open(
        "report.json",
        "w",
    ) as f:
        f.write(
            json.dumps(
                {
                    "requests_count": REQUESTS_COUNT,
                    "success_count": len(
                        [
                            response
                            for response in results
                            if response.status_code == 200
                        ]
                    ),
                    "elapsed_time": t2 - t1,
                }
            )
        )


asyncio.run(main())

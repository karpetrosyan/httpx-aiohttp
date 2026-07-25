from __future__ import annotations

from unittest.mock import patch

import pytest

from httpx_aiohttp import HttpxAiohttpClient
from httpx_aiohttp.httpx2 import Httpx2AiohttpClient
from httpx_aiohttp.httpx2.transport import AiohttpResponseStream as Httpx2AiohttpResponseStream
from httpx_aiohttp.transport import AiohttpResponseStream

CLIENTS = [
    (HttpxAiohttpClient, AiohttpResponseStream),
    (Httpx2AiohttpClient, Httpx2AiohttpResponseStream),
]


@pytest.mark.anyio
@pytest.mark.parametrize("client_cls,stream_cls", CLIENTS)
async def test_response_is_closed_after_request(client_cls, stream_cls) -> None:
    client = client_cls()

    original_aclose = stream_cls.aclose
    call_count = 0

    async def spy_aclose(self):
        nonlocal call_count
        call_count += 1
        return await original_aclose(self)

    with patch.object(stream_cls, "aclose", spy_aclose):
        await client.get("https://httpbin.org/get", timeout=600)

        assert call_count == 1

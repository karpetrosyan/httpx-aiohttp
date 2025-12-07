from unittest.mock import patch

import pytest

from httpx_aiohttp import HttpxAiohttpClient
from httpx_aiohttp.transport import AiohttpResponseStream


@pytest.mark.anyio
async def test_response_is_closed_after_request() -> None:
    client = HttpxAiohttpClient()

    original_aclose = AiohttpResponseStream.aclose
    call_count = 0

    async def spy_aclose(self):
        nonlocal call_count
        call_count += 1
        return await original_aclose(self)

    with patch.object(AiohttpResponseStream, "aclose", spy_aclose):
        await client.get("https://httpbin.org/get", timeout=600)

        assert call_count == 1

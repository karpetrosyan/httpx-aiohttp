from __future__ import annotations

import contextlib

import httpx
import typing
from aiohttp import ClientTimeout
from aiohttp.client import ClientSession, ClientResponse
import aiohttp

AIOHTTP_EXC_MAP = {
    aiohttp.ServerTimeoutError: httpx.TimeoutException,
    aiohttp.ConnectionTimeoutError: httpx.ConnectTimeout,
    aiohttp.SocketTimeoutError: httpx.ReadTimeout,
    aiohttp.ClientConnectorError: httpx.ConnectError,
    aiohttp.ClientPayloadError: httpx.ReadError,
    aiohttp.ClientProxyConnectionError: httpx.ProxyError,
}


@contextlib.contextmanager
def map_aiohttp_exceptions() -> typing.Iterator[None]:
    try:
        yield
    except Exception as exc:
        mapped_exc = None

        for from_exc, to_exc in AIOHTTP_EXC_MAP.items():
            if not isinstance(exc, from_exc):  # type: ignore
                continue
            if mapped_exc is None or issubclass(to_exc, mapped_exc):
                mapped_exc = to_exc

        if mapped_exc is None:  # pragma: no cover
            raise

        message = str(exc)
        raise mapped_exc(message) from exc


class AiohttpResponseStream(httpx.AsyncByteStream):
    CHUNK_SIZE = 1024 * 16

    def __init__(self, aiohttp_response: ClientResponse) -> None:
        self._aiohttp_response = aiohttp_response

    async def __aiter__(self) -> typing.AsyncIterator[bytes]:
        with map_aiohttp_exceptions():
            async for chunk in self._aiohttp_response.content.iter_chunked(
                self.CHUNK_SIZE
            ):
                yield chunk

    async def aclose(self) -> None:
        with map_aiohttp_exceptions():
            await self._aiohttp_response.__aexit__(None, None, None)


class AiohttpTransport(httpx.AsyncBaseTransport):
    def __init__(
        self, client: ClientSession | typing.Callable[[], ClientSession]
    ) -> None:
        self.client = client

    async def handle_async_request(
        self,
        request: httpx.Request,
    ) -> httpx.Response:
        timeout = request.extensions.get("timeout", {})
        sni_hostname = request.extensions.get("sni_hostname")

        if not isinstance(self.client, ClientSession):
            self.client = self.client()

        with map_aiohttp_exceptions():
            try:
                data = request.content
            except httpx.RequestNotRead:
                data = request.stream
                request.headers.pop("transfer-encoding", None)  # handled by aiohttp

            response = await self.client.request(
                method=request.method,
                url=str(request.url),
                headers=request.headers,
                data=data,
                allow_redirects=False,
                auto_decompress=False,
                compress=False,
                timeout=ClientTimeout(
                    sock_connect=timeout.get("connect"),
                    sock_read=timeout.get("read"),
                    connect=timeout.get("pool"),
                ),
                server_hostname=sni_hostname,
            ).__aenter__()

        return httpx.Response(
            status_code=response.status,
            headers=response.headers,
            content=AiohttpResponseStream(response),
            request=request,
        )

    async def aclose(self) -> None:
        if isinstance(self.client, ClientSession):
            await self.client.close()

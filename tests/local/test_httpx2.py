from pathlib import Path

import httpx2
import pytest

from httpx_aiohttp.httpx2 import AiohttpTransport, Httpx2AiohttpClient

PACKAGE_DIR = Path(__file__).resolve().parents[2] / "src" / "httpx_aiohttp"

HTTPX2_IMPORT_LINE = "import httpx2 as httpx"


@pytest.mark.parametrize("module", ["transport.py", "client.py"])
def test_httpx2_modules_stay_in_sync(module: str) -> None:
    """The httpx2 variant modules must be identical to the httpx ones,
    except for the httpx2 import and the client class name."""
    original = (PACKAGE_DIR / module).read_text()
    variant = (PACKAGE_DIR / "httpx2" / module).read_text()

    normalized = variant.replace(HTTPX2_IMPORT_LINE, "import httpx").replace(
        "Httpx2AiohttpClient", "HttpxAiohttpClient"
    )
    assert normalized == original


def test_client_subclasses_httpx2_async_client() -> None:
    assert issubclass(Httpx2AiohttpClient, httpx2.AsyncClient)


def test_httpx2_client_uses_aiohttp_transport() -> None:
    client = Httpx2AiohttpClient()
    assert isinstance(client._transport, AiohttpTransport)


def test_httpx2_client_respects_explicit_transport() -> None:
    transport = AiohttpTransport()
    client = Httpx2AiohttpClient(transport=transport)
    assert client._transport is transport

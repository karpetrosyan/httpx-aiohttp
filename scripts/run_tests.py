import sys

import httpx
import pytest

from httpx_aiohttp import AiohttpTransport
from httpx_aiohttp.client import HttpxAiohttpClient

httpx.AsyncClient = HttpxAiohttpClient
httpx.AsyncHTTPTransport = AiohttpTransport

retcode = pytest.main(
    ["--config-file=tests/httpx/pyproject.toml", "--tb=short", "-W", "ignore::ResourceWarning"] + sys.argv[1:]
)
exit(retcode)

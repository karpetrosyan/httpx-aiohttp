import httpx


class ClientConnectionError(httpx.ConnectTimeout, httpx.PoolTimeout):
    """Raised when a connection to the server cannot be established."""

    pass

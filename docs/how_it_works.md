# How it works

## HTTPX's split design

It's very important to understand that httpx itself is not making any requests, not opening any connections, or doing such things—it just delegates that work to another library.

You can think of httpx as a sans-io library—it doesn't perform any IO operations, but instead has a great design that allows you to bring your own IO. It comes with a default library for IO called [httpcore](https://github.com/encode/httpcore), but you can use another one if you encounter issues with it.

There is a [wonderful talk](https://www.youtube.com/watch?v=JkCTZB57opI) by the author of those libraries (Tom Christie); you can also take a look for more context.

In a nutshell, httpx connects to the underlying HTTP implementation through the transport interface, which has a single method (+ some startup/teardown methods with the default implementation) called `handle_request` that looks like this:

```python
class BaseTransport:
    def __enter__(self: T) -> T:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        self.close()

    def handle_request(self, request: Request) -> Response:
        raise NotImplementedError()

    def close(self) -> None:
        ...
```

And for async one:

```python
class AsyncBaseTransport:
    async def __aenter__(self: A) -> A:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        await self.aclose()

    async def handle_async_request(
        self,
        request: Request,
    ) -> Response:
        raise NotImplementedError()

    async def aclose(self) -> None:
        pass
```

This means you can write your own transports that connect to other low-level implementations such as aiohttp, urllib3, or curl. You may have noticed that you can make requests to [ASGI](https://www.python-httpx.org/advanced/transports/#asgi-transport) and [WSGI](https://www.python-httpx.org/advanced/transports/#wsgi-transport) apps directly with httpx—this is because someone wrote transports that connect to these apps.

This library implements the AsyncBaseTransport interface to connect httpx to aiohttp, so all the high-level operations are handled by httpx while delegating network layer tasks to aiohttp.

!!! warning
    When you write your own transport, you should ensure that the underlying implementation doesn't handle ANYTHING except the actual request sending and proxy connection handling, so all the high-level tasks will be handled by httpx and only by it! You won't have duplicate compression, authentication, or redirect handling—you should disable all of these features in the underlying implementation.

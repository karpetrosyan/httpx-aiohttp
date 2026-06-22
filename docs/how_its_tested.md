# How it's tested?

httpx-aiohttp uses httpx as a submodule and runs all the original httpx tests while mocking the underlying transport, so our new custom transport will be used during tests.

There is a simple script in the `./scripts/run_tests.py` file that mocks the default transport and invokes pytest programmatically. Currently, we are passing all 1200+ tests.

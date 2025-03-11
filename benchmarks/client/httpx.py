# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx>=0.28.1",
# ]
# ///
import os
import httpx

SERVER_URL = os.getenv("SERVER_URL")

if SERVER_URL is None:
    raise RuntimeError("SERVER_URL environment variable is not set")

# write your benchmark code using any HTTP client
response = httpx.get(SERVER_URL)
print(response)
# somehow print results so it will be possible to grab them for the report

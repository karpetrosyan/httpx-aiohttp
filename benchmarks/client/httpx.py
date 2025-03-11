# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx>=0.28.1",
# ]
# ///

import subprocess

# Perform a simple cURL GET request
curl_command = ["curl", "-X", "GET", "http://server:8000"]
response = subprocess.run(curl_command, capture_output=True, text=True)

# Print the response
print(response.stdout)

# import os
# import httpx
#
# SERVER_URL = os.getenv("SERVER_URL")
#
# if SERVER_URL is None:
#     raise RuntimeError("SERVER_URL environment variable is not set")
#
# # write your benchmark code using any HTTP client
# response = httpx.get(SERVER_URL)
# print(response)
# somehow print results so it will be possible to grab them for the report

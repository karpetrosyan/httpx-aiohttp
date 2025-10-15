# Changelog

## 0.1.9 (15th October, 2025)

- Properly close the underlying aiohttp response after reading the content.

## 0.1.8 (4th July, 2025)

- Don't include `Content-Type` to any empty request.

## 0.1.7 (4th July, 2025)

- Don't include `Content-Type` to empty get requests. (#20)

## 0.1.6 (14th June, 2025)

- Add `HttpxAiohttpClient` class 
- Test the aiohttp-powered transport with httpx tests

## 0.1.3 (24th May, 2025)

- Fix streaming requests (#3)

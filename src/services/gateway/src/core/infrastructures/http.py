import httpx

class HTTPClient:
    async def __call__(self):
        async with httpx.AsyncClient() as client:
            yield client
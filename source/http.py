import httpx

from starlette.datastructures import URL, QueryParams


async def request(method: str, url: URL, params: QueryParams = None):
    async with httpx.AsyncClient() as client:
        r = await client.request(method, url)

    if 400 <= r.status_code <= 599:
        return
    else:
        return {"status_code": r.status_code, "data": r.json}


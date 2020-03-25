from typing import Dict

import httpx

from starlette.datastructures import URL, QueryParams


async def request(method: str, url: URL, params: QueryParams = None) -> Dict:
    async with httpx.AsyncClient() as client:
        req = client.build_request(method, url, params)
        resp = await client.send(req)

    if not resp.is_error:
        return {"status": resp.status_code, "data": resp.json()}
    # if 400 <= resp.status_code <= 599:
    else:
        return {
            "status": resp.status_code,
            "errors": [
                {"code": resp.status_code, "detail": resp.reason_phrase}
            ],
        }

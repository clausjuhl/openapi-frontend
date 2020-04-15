from typing import Dict

import httpx

from starlette.datastructures import QueryParams


async def _request(method: str, url: str, params: QueryParams = None) -> Dict:
    async with httpx.AsyncClient() as client:
        req = client.build_request(method, url)
        resp = await client.send(req)

        if not resp.is_error:
            return {"status": resp.status_code, "data": resp.json()}
        else:
            return {
                "status": resp.status_code,
                "errors": [
                    {"code": resp.status_code, "detail": resp.reason_phrase}
                ],
            }


async def get_request(url: str, params: QueryParams = None) -> Dict:
    return await _request("GET", url, params)

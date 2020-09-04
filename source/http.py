from typing import Dict

import httpx

from starlette.datastructures import QueryParams

"""
Returns http-responses ("errors" or "data") as key-normalized dicts.
Openaws has its own status_codes inside the response
"""


def _error(code, detail):
    return {"errors": [{"code": code, "detail": detail}]}


async def _request(method: str, url: str, params: QueryParams = None) -> Dict:
    async with httpx.AsyncClient() as client:
        req = client.build_request(method, url, params=params)
        resp = await client.send(req)

    # network (http) error (via httpx)
    if resp.is_error:
        return _error(resp.status_code, resp.reason_phrase)

    # syntax-error
    try:
        data = resp.json()
    except ValueError as e:
        return _error(500, "Unable to parse API-response as json")

    # if openaws, payload includes a "status_code"
    if "status_code" in data.keys():
        code = data.get("status_code")

        # openaws-errors
        if code in [1, 3]:
            return _error(404, "The resource could not be found")
        if code == 2:
            return _error(400, "The resource has been deleted")

        data.pop("status_code")
        # openaws-success
        # return {"data": data.get("result")}
    return data
    # else non-openaws-success
    # return {"data": data}


async def get_request(url: str, params: QueryParams = None) -> Dict:
    return await _request("GET", url, params)


def get_request_sync(url: str, params: QueryParams = None) -> Dict:
    resp = httpx.get(url, params=params)
    # network (http) error (via httpx)
    if resp.is_error:
        return _error(resp.status_code, resp.reason_phrase)

    # syntax-error
    try:
        data = resp.json()
    except ValueError as e:
        return _error(500, "Unable to parse API-response as json")

    # if openaws, payload includes a "status_code"
    if "status_code" in data.keys():
        code = data.get("status_code")

        # openaws-errors
        if code in [1, 3]:
            return _error(404, "The resource could not be found")
        if code == 2:
            return _error(400, "The resource has been deleted")

        data.pop("status_code")
        # openaws-success
        # return {"data": data.get("result")}
    return data
    # else non-openaws-success
    # return {"data": data}

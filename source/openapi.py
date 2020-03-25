import json
from typing import Dict

from starlette.datastructures import URL, QueryParams

from source import settings, http


# def _api_request(self, path, method="get", params=None, data=None):
#     # Always returns a dict with 'status_code' plus 'result' or 'status_msg'
#     if method == "get":
#         r = requests.get("/".join([self.host, path]), params=params)
#     else:
#         r = requests.post("/".join([self.host, path]), data=data)

#     try:
#         r_to_dict = json.loads(r.content)
#         return r_to_dict
#     except ValueError as e:
#         return {"status_code": 5, "status_msg": str(e)}


async def _error_response(code: int, msg: str, id_: int = None) -> Dict:
    error = dict()
    error["code"] = code
    error["msg"] = msg
    if id_:
        error["id"] = id_

    return {"errors": [error]}


async def _response(response: Dict) -> Dict:
    # forward any error-responses from httpx
    if response.get("errors"):
        return response

    # parse response from openaws and aarhusiana
    data = response.get("data")
    if data.get("status_code") == 0:
        return data.get("result")

    elif data.get("status_code") == 1:
        return _error_response(404, "The resource does not exist", id=resource)

    elif data.get("status_code") == 2:
        return _error_response(
            400, "The resource has been deleted", id=resource
        )

    else:
        return _error_response(
            data.get("status_code"), data.get("status_msg"), id=resource
        )


async def get_resource(collection: str, item: int):
    if collection not in settings.resource_endpoints:
        return _error_response(
            404, "BAD REQUEST. No such collection: " + collection
        )

    url = f"{settings.resource_host}/{settings.resource_endpoints[collection]}/{str(item)}"
    r = http.get_request(url)

    return _response(r.get("data"))


# 'batch_records' from ClientInterface reformatted
def multi_get_records(self, id_list=None):
    if not id_list:
        return []

    data = {"view": "record", "oasid": json.dumps(id_list)}
    r = self._api_request(path="resolve_records_v2", method="post", data=data)

    if r.get("status_code") == 0:
        return r.get("result")

    else:
        return {
            "errors": [
                {"code": r.get("status_code"), "msg": r.get("status_msg")}
            ]
        }


# 'resolve_params'
def get_entity_labels(self, resource_list):
    # resource_list: [('collection', '4'), ('availability', '2')]
    r = self._api_request("resolve_params", params=resource_list)

    if r.get("status_code") == 0:
        output = []
        for key, value in r.get("resolved_params").items():
            for k, v in value.items():
                d = {"resource": key, "id": k, "label": v.get("display_label")}
                output.append(d)
        return {"result": output}
    else:
        return {
            "errors": [
                {"code": r.get("status_code"), "msg": r.get("status_msg")}
            ]
        }
